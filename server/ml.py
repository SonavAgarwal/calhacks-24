import torch
from torchvision import models, transforms
from PIL import Image
# from PIL import Image as PILImage
from typing import List
from image_embedding import get_image_description_vector_embedding
import hyperbolic
import stitcher
from predict import segment, get_unique_filename, show_masks_and_boxes_on_image
import threading
from chroma import add_image_vector_to_collection
from aws import upload_image_to_s3
from db import update_item
import io
from io import BytesIO
import base64
import numpy as np

def get_items_from_image(image, debug: bool = False):
    """
    Args
    -   image: PIL Image object
    
    Returns list of cropped segmented 
    images of items (PIL.Image)
    from a single panoramic image. 
    """
    segmented_images, segmented_images_bboxes, transparent_segmented_images = segment(image, debug)
    return segmented_images, segmented_images_bboxes, transparent_segmented_images

def get_image_data(image, transparent_image):
    """
    Given an Image, returns a tuple of all the image data

    Returns:
    - (vectorEmbedding, name, desc, category)
    """

    results = hyperbolic.process_images([transparent_image])
    if not results:
        return None
    else:
        result = results[0]

        name = result['name'] # PRANAV: get name
        desc = result['description'] # PRANAV: get desc
        category = result['category'] # PRANAV: get category
        price = result['price']
        vector_embedding = get_image_description_vector_embedding(name+": "+desc)

        return (vector_embedding, name, desc, category, price)

def get_image_filtered_list_data(images, transparent_images, bboxes: List[List[int]]):
    """
    Given a list of images (tensors) returns a list of
    tuples where each tuple contains important data of the image

    Args:
    - list of unfiltered images
    - list of bounding boxes of the images

    returns Tuple[vectorEmbedding, name, desc, category], List[Image]
    """
    res = []
    filtered_images = []
    for image, transparent_image, bbox in zip(images, transparent_images, bboxes):
        img_data = get_image_data(image, transparent_image)
        if img_data: # only if image data is valid append
            res.append(img_data)
            filtered_images.append(transparent_image)
    return res, filtered_images

def process_video(video: object, s3: object, before=True, status='pending'):
    """
    Args
    - video: a video file of a room
    - s3: s3 client
    - before(bool): boolean of whether video is from before damage (True) or after image (False)
    - status(str): status of item images generated by video (pending, rejected, etc.)

    Return
    - List[String]: response of successful image upload
    """

    # 1) load panorama photo from video
    panorama_image = stitcher.create_panorama(video)
    print("Panorama image created.")
    print("pano type", type(panorama_image))
    print("pano shape", panorama_image.shape)

    # 2) get items from the image
    segmented_images, segmented_images_bboxes, transparent_segmented_images = get_items_from_image(panorama_image)

    # 3) get image data from the segmented images
    image_data_list, filtered_images = get_image_filtered_list_data(segmented_images, transparent_segmented_images, segmented_images_bboxes)
    
    # 4) upload ALL (item) IMAGE DATA to chromadb using vector embedding + name, desc, category, price
    image_urls = []
    
    for file in filtered_images:
        buffered_img = BytesIO()
        file.save(buffered_img, format="PNG")
        buffered_img.seek(0)
        image_url = upload_image_to_s3(s3, buffered_img)
        image_urls.append(image_url)

    for url, data in zip(image_urls, image_data_list):
        vector_embedding, name, desc, category, price = data

        # Add image to chromadb
        image_id, item_id = add_image_vector_to_collection(vector_embedding, url, before, status)
        print(f"Added image with item_id {image_id} to the collection.")

        # Update item in SQLite db with image data
        update_item(item_id, name, desc, category, price, before)
    

    # filtered_images are the images we want to display on frontend
    return image_urls

def process_image(image, s3: object, before=True, status='pending'):
    """
    Args
    - image: a single image of a room
    - s3: s3 client
    - before(bool): boolean of whether video is from before damage (True) or after image (False)
    - status(str): status of item images generated by video (pending, rejected, etc.)

    Return
    - List[String]: response of successful image upload
    """
    image = Image.open(io.BytesIO(image.read()))

    image = image.convert('RGB')
    image = np.asarray(image)

    # print image shape
    print("image type", type(image))
    print("image shape", image.shape)


    # 1) get items from the image
    print("Processing image...")
    segmented_images, segmented_images_bboxes, transparent_segmented_images = get_items_from_image(image)

    print("Segmented images")
    # 2) get image data from the segmented images
    image_data_list, filtered_images = get_image_filtered_list_data(segmented_images, transparent_segmented_images, segmented_images_bboxes)
    
    print("Image data list")
    # 3) upload ALL (item) IMAGE DATA to chromadb using vector embedding + name, desc, category, price
    image_urls = []
    
    for file in filtered_images:
        buffered_img = BytesIO()
        file.save(buffered_img, format="PNG")
        buffered_img.seek(0)
        image_url = upload_image_to_s3(s3, buffered_img)
        image_urls.append(image_url)

    for url, data in zip(image_urls, image_data_list):
        vector_embedding, name, desc, category, price = data

        # Add image to chromadb
        image_id, item_id = add_image_vector_to_collection(vector_embedding, url, before, status)
        print(f"Added image with item_id {image_id} to the collection.")

        # Update item in SQLite db with image data
        update_item(item_id, name, desc, category, price, before)
    

    # filtered_images are the images we want to display on frontend
    return image_urls