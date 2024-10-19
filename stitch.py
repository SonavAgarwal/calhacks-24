from stitching import Stitcher
import cv2
import os

import base64
import requests
from io import BytesIO
from PIL import Image
import time
from typing import Any, Dict
 
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




def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string



def get_json(img):
    pano = create_panorama(img)
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
                    {"type": "text", "text": "List ALL the unique objects in this image of even small value, including their estimate monetary value. Output format MUST be json, similar to the following: {'item':{'name':'','quantity':'','cost_per_item':''},}. DO NOT respond with anything other than the json. start json output here:"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                    },
                ],
            }
        ],
        "model": "Qwen/Qwen2-VL-7B-Instruct",
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    response = requests.post(api, headers=headers, json=payload)
    print(response.json())
    return response.json()['choices'][0]['message']['content']



@agent.on_rest_get("/rest/get", Response)
async def handle_get(ctx: Context) -> Dict[str, Any]:
    ctx.logger.info("Received GET request")
    return {
        "timestamp": int(time.time()),
        "text": get_json("test1.mov"),
        "agent_address": ctx.agent.address,
    }
 
 
if __name__ == "__main__":
    agent.run()