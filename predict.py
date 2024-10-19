import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import gc
from PIL import Image
import os
from transformers import pipeline, SamModel, SamProcessor
from ultralytics import YOLO
import supervision as sv

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

def segment(img_path):
  yolo_model = YOLO("yolov8n.pt")
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  model = SamModel.from_pretrained("facebook/sam-vit-huge").to(device)
  processor = SamProcessor.from_pretrained("facebook/sam-vit-huge")

  raw_image, bboxes = detect_objects(img_path, yolo_model)
  masks = segment_image(raw_image, bboxes, model, processor, device)

  segmented_images = []
  for mask, bbox in zip(masks, bboxes):
      x_min, y_min, x_max, y_max = bbox
      cropped_image = raw_image.crop((x_min, y_min, x_max, y_max))
      mask_pil = Image.fromarray((mask.squeeze().numpy() * 255).astype(np.uint8))
      mask_resized = mask_pil.resize(cropped_image.size, resample=Image.BILINEAR)
      segmented_image = Image.composite(cropped_image, Image.new("RGB", cropped_image.size), mask_resized)
      segmented_images.append(segmented_image)

  return segmented_images

# Example usage:
img_path = "./images/pano.jpg"
segmented_images = segment(img_path)
for i, img in enumerate(segmented_images):
    img.save(f"./predictions/segmented_{i}.png")