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
        List the following details for the item in this image:
        {"name": <string>, "description": <string>, "category": <string>, "price": <float>, "is_object": <bool>}.
        category can be one of the following: Electronics, Appliances, Furniture, Kitchenware, Containers, Clothing and Accessories, Artwork and Antiques, Toiletry, Tools and Equipment, Toys and Games, Home Decor, Bedding and Linens, Kitchenware, Hobby and Craft Supplies, Media and Collectibles, Medical Equipment, Pet Supplies, Food, Firearms
        is_object should be true for recognizable objects/furniture, false for walls, people, and unrecognizable things.
        price is the estimated dollar value of the object.
        json output should be one dict like the following example {"name": <string>, "description": <string>, "category": <string>, , "price": <float>, "is_object": <bool>}
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
        "top_p": 0.9,
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

        item_details = get_item_details_from_image(image)
        if item_details:
            # Parse the JSON response
            item_json = json.loads(item_details)
            
            # Filter out items that are not objects
            if item_json.get("is_object", False):
                items.append(item_json)
    
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

# Example usage:
# Provide a list of image file paths
file_paths = [f'objects/{e}' for e in os.listdir("objects")]

# Load images from file paths
images = load_images_from_files(file_paths)

# Process the loaded images
filtered_items = process_images(images)


# Print the filtered results nicely
print("Filtered Items (Objects):")
for item in filtered_items:
    print(f"Name: {item['name']}")
    print(f"Description: {item['description']}")
    print(f"Category: {item['category']}")
    print(f"Price: {item['price']}")
    print("-" * 30)