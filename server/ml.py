import torch
print(2)
from torchvision import models, transforms
print(2)

from typing import List
from image_embedding import get_image_vector_embedding
print(2)
import hyperbolic
print(2)
import stitcher
from predict import segment, get_unique_filename, show_masks_and_boxes_on_image
print(2)
import threading
print(2)
from PIL.Image import Image, open
print(2)

def get_items_from_image(img_path: str, debug: bool = False):
    """
    Args
    -   img_path: path to the image
    
    Returns list of cropped segmented 
    images of items (PIL.Image)
    from a single panoramic image. 
    """
    segmented_images, segmented_images_bboxes, transparent_segmented_images = segment(img_path, debug)
    return segmented_images, segmented_images_bboxes, transparent_segmented_images

def load_image(img_path: str):
    """
    Given a image path returns an Image.
    """
    image = open(img_path).convert('RGB')
    return image

def get_image_data(image: Image):
    """
    Given an Image, returns a tuple of all the image data

    Returns:
    - (vectorEmbedding, name, desc, category)
    """

    vector_embedding = get_image_vector_embedding(image)

    results = hyperbolic.process_images([image])
    if not results:
        return None
    else:
        result = results[0]

        name = result['name'] # PRANAV: get name
        desc = result['description'] # PRANAV: get desc
        category = result['category'] # PRANAV: get category
        price = result['price']
        return (vector_embedding, name, desc, category, price)

def get_image_filtered_list_data(images: List[Image], bboxes: List[List[int]]):
    """
    Given a list of images (tensors) returns a list of
    tuples where each tuple contains important data of the image

    Args:
    - list of unfiltered images
    - list of bounding boxes of the images

    returns Tuple[vectorEmbedding, name, desc, category]
    """
    res = []
    for image, bbox in zip(images, bboxes):
        img_data = get_image_data(image)
        if img_data: # only if image data is valid append
            res.append(img_data)
    return res

def process_video(video_path: str, debug=False):
    """
    Args
    - video: a video file of a room

    Return
    - String: response of successful video upload
    """

    # 1) load video from video_path
    stitcher.create_panorama(video_path)

    # 2) get items from the image
    segmented_images, segmented_images_bboxes, transparent_segmented_images = get_items_from_image("pano.png", debug=debug)

    # 3) get image data from the segmented images
    image_data = get_image_filtered_list_data(segmented_images, segmented_images_bboxes)
    # 7.1) upload vector embedding + METADATA to chromadb
    # 7.2) upload name, desc, category, price 

    pass

process_video("../test3.mov", debug=True)