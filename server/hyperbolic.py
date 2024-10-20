import os
import cv2
import base64
import requests
import io
import json
from PIL import Image

def encode_image(image):
    """Encodes a PIL image to a base64 string, converting RGBA to RGB if necessary."""
    if image.mode == 'RGBA':
        image = image.convert('RGB')  # Convert to RGB mode if the image has an alpha channel
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def get_item_details_from_image(image):
    """Sends an image to the vision model and retrieves item details."""
    base64_img = encode_image(image)

    api = "https://api.hyperbolic.xyz/v1/chat/completions"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvcmNhLnByYW5hdkBnbWFpbC5jb20iLCJpYXQiOjE3MjkzMjA2NTh9.qjszlFbnDKQVXjrNp6eotZnVKbbsM6nc7_cJ36grBT8"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Prepare the message content
    message_content = [
        {"type": "text", "text": """
        List the following details for the item outlined by a thin red line in this image:
        {"name": <string>, "description": <string>, "category": <string>, "price": <float>, "is_object": <int>}.
        category can be one of the following: Electronics, Appliances, Furniture, Kitchenware, Containers, Clothing and Accessories, Toiletry, Tools and Equipment, Toys and Games, Home Decor, Bedding and Linens, Kitchenware, Hobby and Craft Supplies, Medical Equipment, Pet Supplies, Pets, Food, Firearms
        is_object should be 1 for recognizable non-human objects/furniture. is_object should be 0 for walls, people, persons, humans, men, women and unrecognizable things. If you are at all unsure about what is outlined in red, say it is unrecognizable and set is_object to 0. You are checking if the thing highlighted by the outline is_object, NOT other objects in the image.
        price is the estimated dollar value of the object.
        json output should be one dict like the following example {"name": <string>, "description": <string>, "category": <string>, , "price": <float>, "is_object": <int>}
        Start JSON output here:
        """},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
    ]

    payload = {
        "messages": [
            {
                "role": "user",
                "content": message_content,
            }
        ],
        "model": "Qwen/Qwen2-VL-7B-Instruct",
        "max_tokens": 32000,
        "temperature": 0.7,
        "top_p": 0.9
    }

    # Make the API request
    response = requests.post(api, headers=headers, json=payload)
    response_json = response.json()

    try:
        item_details = response_json['choices'][0]['message']['content'].replace('json','').replace('```','')
        return item_details
    except KeyError:
        print("Error with API response:", response_json)
        return None

def process_images(images):
    """Processes a list of images, filters non-objects, and prints the result."""
    items = []
    
    for image in images:
        print("Processing image...")
        retries = 3
        while retries > 0:
            try:
              item_details = get_item_details_from_image(image)
              if item_details:
                  item_json = json.loads(item_details)

              if any(e in item_details.lower() for e in ["unrecognizable", "person","man","woman","human"]):
                break
              if item_json.get("is_object", False):
                items.append(item_json)
              break
            except Exception as e:
              print(f"Error processing image: {e}")
              print(item_details)
              retries -= 1
              if retries == 0:
                  print("Failed to process image after 3 attempts.")
    
    return items

def load_images_from_files(file_paths):
    """Loads images from a list of file paths and returns a list of PIL Image objects."""
    images = []
    
    for file_path in file_paths:
        try:
            image = Image.open(file_path)
            images.append(image)
        except Exception as e:
            print(f"Error loading image {file_path}: {e}")
    
    return images
