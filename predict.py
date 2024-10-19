import torch
import transformers
from transformers import pipeline
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import gc
from PIL import Image
import requests
from ultralytics import YOLO
import os

def show_mask(mask, ax, random_color=False):
  if random_color:
    color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
  else:
    color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
  h, w = mask.shape[-2:]
  mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
  ax.imshow(mask_image)
  del mask
  gc.collect()

def show_masks_on_image(raw_image, masks, bboxes, save_path):
  plt.imshow(np.array(raw_image))
  ax = plt.gca()
  ax.set_autoscale_on(False)
  for mask in masks:
    show_mask(mask, ax=ax, random_color=True)
  for bbox in bboxes:
    x_min, y_min, x_max, y_max = bbox[0]
    rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=2, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
  plt.axis("off")
  plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
  plt.close()
  del mask
  gc.collect()

# Load the image
img_path = "./images/Welikson-Osborne-Harvey-0009.jpg"
raw_image = Image.open(img_path).convert("RGB")

# Use YOLOv8 to get bounding boxes
model = YOLO("yolov8n.pt")
results = model(img_path)

# Extract bounding boxes
bboxes = []
for result in results:
  for box in result.boxes:
    bboxes.append(box.xyxy.numpy())

# Prepare prompts for SAM
prompts = []
for bbox in bboxes:
  x_min, y_min, x_max, y_max = bbox[0]
  prompts.append({
    "bbox": [x_min, y_min, x_max, y_max]
  })

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Use SAM to generate masks
transformers.logging.set_verbosity_info()
generator = pipeline("mask-generation", model="facebook/sam-vit-huge", device=device)
outputs = generator(raw_image, prompts=prompts, points_per_batch=256)
masks = outputs["masks"]

os.makedirs("./predictions", exist_ok=True)
save_path = "./predictions/masked_image.png"
show_masks_on_image(raw_image, masks, bboxes, save_path)