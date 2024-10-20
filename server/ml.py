import torch
from torchvision import models, transforms
from PIL.Image import Image, open
from typing import List
from image_embedding import get_image_vector_embedding
import hyperbolic

def get_items_from_image(image):
    """
    Args
    -   image: idk like a 2D RGB tensor ??
    
    Returns list of cropped segmented 
    images of items (also 2D RGB tensors??) 
    from a single panoramic image. 
    """
    pass

def filter_images(images: list):
    """
    removes irrelavant images from list of cropped images

    Returns: filtered list of cropped images
    """
    pass

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

def get_image_filtered_list_data(images: List[Image]):
    """
    Given a list of images (tensors) returns a list of
    tuples where each tuple contains important data of the image

    Args:
    - list of unfiltered images

    returns Tuple[vectorEmbedding, name, desc, category]
    """
    res = []
    for image in images:
        img_data = get_image_data(image)
        if img_data: # only if image data is valid append
            res.append(img_data)
    return res

def process_video(video_path: str):
    """
    Args
    - video: a video file of a room

    Return
    - String: response of successful video upload
    """

    # 1) load video from video_path

    # 2) convert video to panoramic

    # 3) YOLO panoramic

    # 4) use YOLO to run SAM on img

    # 5) filter out bad imgs with Hyperbolic

    # 6) get data of all the filtered images

    # 7.1) upload vector embedding + METADATA to chromadb
    # 7.2) upload name, desc, category, price 
    


    pass