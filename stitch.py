from stitching import Stitcher
import cv2
import os
import json
import base64
import requests
from io import BytesIO
from PIL import Image
import time
from typing import Any, Dict
import numpy as np
from uagents import Agent, Context, Model

os.environ['KMP_WARNINGS'] = '0'


class Response(Model):
    timestamp: int
    text: str
    agent_address: str
 
 
# You can also use empty models to represent empty request/response bodies
class EmptyMessage(Model):
    pass
 
 
agent = Agent(name="Rest API")



def add_black_borders_to_square(image):
    """
    Adds black borders to make a rectangular image square.

    :param image: The input image read with cv2 (numpy array).
    :return: The square image with black borders (padded).
    """
    # Get the current dimensions of the image
    height, width, _ = image.shape

    # Determine the size of the square (the larger of width and height)
    max_size = max(height, width)

    # Calculate the padding needed for each side
    top_padding = (max_size - height) // 2
    bottom_padding = max_size - height - top_padding
    left_padding = (max_size - width) // 2
    right_padding = max_size - width - left_padding

    # Apply the padding (borders) using cv2.copyMakeBorder
    square_image = cv2.copyMakeBorder(
        image,
        top_padding, bottom_padding, left_padding, right_padding,
        borderType=cv2.BORDER_CONSTANT,
        value=[0, 0, 0]  # Black border
    )

    return square_image


def create_panorama(path):
    # Set up video file
    video_path = path

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # Get video frame rate (fps)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Extract 1/10th of the frames
    # frame_interval = int(fps / 10)  # Capture one frame for every 0.1 seconds

    frame_number = 0
    extracted_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break  # Video is finished or cannot read frame

        # Add every 1/10th frame to the list
        if frame_number % 10 == 0:
            # resized_frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
            extracted_frames.append(frame)

        frame_number += 1

    # Release the video capture object
    cap.release()

    print(f"read frames {len(extracted_frames)}")
    stitcher = Stitcher()
    settings = {"detector": "sift", "confidence_threshold": 0.05,"matches_graph_dot_file":False,"crop":False}
    stitcher = Stitcher(**settings)

    print("stritiching")
    panorama = stitcher.stitch(extracted_frames)
    
    return panorama



def display_image(json_data):
    items_data = json.loads(json_data)

    # Load the image on which you want to plot the bounding boxes
    image_path = "pano.jpg"  # replace this with your image path
    image = cv2.imread(image_path)

    # Check if the image loaded successfully
    if image is None:
        print("Error: Could not load the image.")
        exit()

    # Loop through items and plot bounding boxes
    for item in items_data:
        item_name = item["item"]["name"]
        for bbox in item["item"]["bounding_boxes"]:
            # Extract the bounding box coordinates
            x1, y1 = bbox["x1"], bbox["y1"]
            x2, y2 = bbox["x2"], bbox["y2"]

            # Draw a rectangle for each bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box
            
            # Put label (item name) on the image
            cv2.putText(image, item_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the image with bounding boxes and labels
    # image = add_black_borders_to_square(image)
    cv2.imwrite("boxes.jpg", image)


def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string



def get_json(img):
    pano = create_panorama(img)
    print('created_pano')
    # pano = add_black_borders_to_square(pano)
    cv2.imwrite("pano.jpg",pano)
    img = Image.open("pano.jpg")
    base64_img = encode_image(img)

    api = "https://api.hyperbolic.xyz/v1/chat/completions"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvcmNhLnByYW5hdkBnbWFpbC5jb20iLCJpYXQiOjE3MjkzMjA2NTh9.qjszlFbnDKQVXjrNp6eotZnVKbbsM6nc7_cJ36grBT8"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": """List ALL the unique items/objects/furniture in this image of even small value, including their estimated monetary value and pixel bounding box in image. Output format MUST be json, similar to the following: {"item":{"name":"","quantity":"","cost_per_item":"", "bounding_boxes":[{"x1":,"x2":,"y1":,"y2":},]}}. DO NOT respond with anything other than the json. start json output here:"""},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                    },
                ],
            }
        ],
        "model": "Qwen/Qwen2-VL-7B-Instruct",
        "max_tokens": 32000,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    print('sent gpt request')
    response = requests.post(api, headers=headers, json=payload)
    print(response.json())
    return response.json()['choices'][0]['message']['content'].replace('json','').replace('```','')



@agent.on_rest_get("/rest/get", Response)
async def handle_get(ctx: Context) -> Dict[str, Any]:
    ctx.logger.info("Received GET request")
    json_data = get_json("test3.mov")
    print("displaying image")
    display_image(json_data)
    return {
        "timestamp": int(time.time()),
        "text": json_data,
        "agent_address": ctx.agent.address,
    }
 
 
if __name__ == "__main__":
    agent.run()