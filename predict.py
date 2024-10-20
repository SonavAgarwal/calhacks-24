import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import gc
from PIL import Image, ImageDraw
import os
from transformers import pipeline, SamModel, SamProcessor
from ultralytics import YOLO
import supervision as sv
import cv2
from torchvision.transforms import ToPILImage

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

def get_unique_filename(base_path):
  if not os.path.exists(base_path):
    return base_path
  base, ext = os.path.splitext(base_path)
  counter = 1
  new_path = f"{base}_{counter}{ext}"
  while os.path.exists(new_path):
    counter += 1
    new_path = f"{base}_{counter}{ext}"
  return new_path

def show_masks_and_boxes_on_image(raw_image, masks, bboxes, save_path):
  save_path = get_unique_filename(save_path)
  plt.imshow(np.array(raw_image))
  ax = plt.gca()
  ax.set_autoscale_on(False)
  for mask in masks:
    for m in mask:
      show_mask(np.array(m), ax=ax, random_color=True)
  for bbox in bboxes:
    x_min, y_min, x_max, y_max = bbox
    rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=1, edgecolor='g', facecolor='none')
    ax.add_patch(rect)
  plt.axis("off")
  plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
  plt.close()
  gc.collect()

def detect_objects(img_path, yolo_model):
  raw_image = Image.open(img_path).convert("RGB")
  results = yolo_model(img_path, conf=0.01)[0]
  results = sv.Detections.from_ultralytics(results).with_nms(threshold=0.05, class_agnostic=True)
  bboxes = [result[0].tolist() for result in results]
  return raw_image, bboxes

def segment_image(raw_image, bboxes, model, processor, device):
  inputs = processor(raw_image, return_tensors="pt").to(device)
  image_embeddings = model.get_image_embeddings(inputs["pixel_values"])

  inputs = processor(raw_image, input_boxes=[bboxes], return_tensors="pt").to(device)
  inputs.pop("pixel_values", None)
  inputs.update({"image_embeddings": image_embeddings})

  with torch.no_grad():
    outputs = model(**inputs, multimask_output=False)

  masks = processor.image_processor.post_process_masks(outputs.pred_masks.cpu(), inputs["original_sizes"].cpu(), inputs["reshaped_input_sizes"].cpu())
  return masks[0]

def segment(img_path, debug=False, padding_ratio=0.2):
    yolo_model = YOLO("yolov8n.pt")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SamModel.from_pretrained("facebook/sam-vit-huge").to(device)
    processor = SamProcessor.from_pretrained("facebook/sam-vit-huge")

    raw_image, bboxes = detect_objects(img_path, yolo_model)
    masks = segment_image(raw_image, bboxes, model, processor, device)
    if debug:
        save_masked_path = get_unique_filename("./predictions/masked_image.png")
        save_boxes_path = get_unique_filename("./predictions/boxes_image.png")

    show_masks_and_boxes_on_image(raw_image, [], bboxes, save_boxes_path)
    show_masks_and_boxes_on_image(raw_image, masks, [], save_masked_path)

    segmented_images = []

    # Loop over the masks and create cropped images with masks outlined
    for i, mask in enumerate(masks):
        mask_np = np.array(mask).squeeze()  # Ensure mask is 2D by removing extra dimensions if present

        # Find the bounding box for the mask by getting min/max coordinates where the mask is present
        y_indices, x_indices = np.where(mask_np > 0)  # Ensure mask is binary
        if len(y_indices) == 0 or len(x_indices) == 0:
            continue  # Skip if mask is empty

        x_min, x_max = np.min(x_indices), np.max(x_indices)
        y_min, y_max = np.min(y_indices), np.max(y_indices)

        # Create a square bounding box around the mask
        bbox_size = max(x_max - x_min, y_max - y_min)

        # Add padding to include more context around the mask
        padding = int(bbox_size * padding_ratio)
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(raw_image.width, x_max + padding)
        y_max = min(raw_image.height, y_max + padding)

        # Crop the image around the padded bounding box
        cropped_image = raw_image.crop((x_min, y_min, x_max, y_max))

        # Convert the cropped image to a format that can be edited with PIL
        cropped_image_np = np.array(cropped_image)
        img_with_outline = Image.fromarray(cropped_image_np)

        # Convert mask to 1-pixel outline using a simple dilation trick
        mask_cropped = mask_np[y_min:y_max, x_min:x_max]
        outline = np.zeros_like(mask_cropped)

        # Create an outline by checking neighbors
        for y, x in zip(*np.where(mask_cropped > 0)):
            if (y > 0 and mask_cropped[y-1, x] == 0) or \
               (y < mask_cropped.shape[0] - 1 and mask_cropped[y+1, x] == 0) or \
               (x > 0 and mask_cropped[y, x-1] == 0) or \
               (x < mask_cropped.shape[1] - 1 and mask_cropped[y, x+1] == 0):
                outline[y, x] = 1  # Mark the boundary

        # Draw the outline on the cropped image in red
        draw = ImageDraw.Draw(img_with_outline)
        for y, x in zip(*np.where(outline > 0)):
            draw.point((x, y), fill="red")

        segmented_images.append(img_with_outline)

    return segmented_images

# Example usage:
img_path = "./images/pano.jpg"
segmented_images = segment(img_path, debug=True)
if not os.path.exists("./predictions/segments"): 
    os.makedirs("./predictions/segments")
for i, img in enumerate(segmented_images):
    img.save(f"./predictions/segments/segmented_{i}.png")