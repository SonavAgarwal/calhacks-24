import torch
from torchvision import models, transforms
from PIL.Image import Image, open
from typing import List
from image_embedding import get_image_vector_embedding
import hyperbolic
import stitcher
from predict import segment, get_unique_filename, show_masks_and_boxes_on_image
import threading
from chroma import add_image_vector_to_collection
from aws import upload_image_to_s3, open_s3_client

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

def get_image_data(image: Image, transparent_image: Image):
    """
    Given an Image, returns a tuple of all the image data

    Returns:
    - (vectorEmbedding, name, desc, category)
    """

    vector_embedding = get_image_vector_embedding(transparent_image)

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

def get_image_filtered_list_data(images: List[Image], transparent_images: List[Image], bboxes: List[List[int]]):
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
      filtered_images.append(image)
  return res, filtered_images

def process_video(video_path: str, s3: object):
  """
  Args
  - video: a video file of a room
  - s3: s3 client

  Return
  - List[String]: response of successful image upload
  """

  # 1) load video from video_path
  stitcher.create_panorama(video_path)

  # 2) get items from the image
  segmented_images, segmented_images_bboxes, transparent_segmented_images = get_items_from_image("pano.png", debug=True)

  # 3) get image data from the segmented images
  image_data, filtered_images = get_image_filtered_list_data(segmented_images, transparent_segmented_images, segmented_images_bboxes)
  # 4.1) upload vector embedding + METADATA to chromadb
  # 4.2) upload name, desc, category, price 
  uploaded_images = []
  
  for file in filtered_images:
      image_url = upload_image_to_s3(s3, file)
      uploaded_images.append(image_url)

  for img, data in zip(filtered_images, image_data):
      vector_embedding, name, desc, category, price = data
      image_id = add_image_vector_to_collection(vector_embedding, name, desc, category, price)
      print(f"Added image with item_id {image_id} to the collection.")

  # filtered_images are the images we want to display on frontend
  return uploaded_images

def process_image(image_path: str, s3: object):
  """
  Args
  - image_path: a single image of a room
  - s3: s3 client

  Return
  - List[String]: response of successful image upload
  """

  # 1) get items from the image
  segmented_images, segmented_images_bboxes, transparent_segmented_images = get_items_from_image(image_path, debug=True)

  # 2) get image data from the segmented images
  image_data, filtered_images = get_image_filtered_list_data(segmented_images, transparent_segmented_images, segmented_images_bboxes)
  # 3.1) upload vector embedding + METADATA to chromadb
  # 3.2) upload name, desc, category, price 
  uploaded_images = []
  
  for file in filtered_images:
      image_url = upload_image_to_s3(s3, file)
      uploaded_images.append(image_url)

  for img, data in zip(filtered_images, image_data):
      vector_embedding, name, desc, category, price = data
      image_id = add_image_vector_to_collection(vector_embedding, name, desc, category, price)
      print(f"Added image with item_id {image_id} to the collection.")

  # filtered_images are the images we want to display on frontend
  return uploaded_images