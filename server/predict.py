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

def show_mask(mask, ax, random_color=False):
    """
    Display a mask on the given axis with optional random color.
    """
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
    """
    Generate a unique filename by appending a counter if the file exists.
    """
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
    """
    Display masks and bounding boxes on an image and save it.
    """
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

def detect_objects(image: Image, yolo_model):
    """
    Detect objects in an image using YOLO model and return the image and bounding boxes.
    """
    results = yolo_model(image, conf=0.01)[0]
    results = sv.Detections.from_ultralytics(results).with_nms(threshold=0.05, class_agnostic=True)
    bboxes = [result[0].tolist() for result in results]
    return image, bboxes

def segment_image(raw_image, bboxes, model, processor, device):
    """
    Segment the image using SAM model and return the masks.
    """
    inputs = processor(raw_image, return_tensors="pt").to(device)
    image_embeddings = model.get_image_embeddings(inputs["pixel_values"])

    inputs = processor(raw_image, input_boxes=[bboxes], return_tensors="pt").to(device)
    inputs.pop("pixel_values", None)
    inputs.update({"image_embeddings": image_embeddings})

    with torch.no_grad():
        outputs = model(**inputs, multimask_output=False)

    masks = processor.image_processor.post_process_masks(outputs.pred_masks.cpu(), inputs["original_sizes"].cpu(), inputs["reshaped_input_sizes"].cpu())
    return masks[0]

def segment(image: Image, debug=False, padding=10):
    """
    Segment objects in an image and return segmented images with masks outlined.
    """
    image = Image.fromarray(image)
    yolo_model = YOLO("yolov8n.pt")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SamModel.from_pretrained("facebook/sam-vit-huge").to(device)
    processor = SamProcessor.from_pretrained("facebook/sam-vit-huge")

    raw_image, bboxes = detect_objects(image, yolo_model)
    masks = segment_image(raw_image, bboxes, model, processor, device)
    if debug:
        if not os.path.exists("./images"):
            os.makedirs("./images")
        save_boxes_path = get_unique_filename("./images/boxes_image.png") 
        show_masks_and_boxes_on_image(raw_image, [], bboxes, save_boxes_path)
        save_masked_path = get_unique_filename("./images/masked_image.png")
        show_masks_and_boxes_on_image(raw_image, masks, [], save_masked_path)

    segmented_images = []
    segmented_images_bboxes = []
    transparent_segmented_images = []
    
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
        bbox_width = x_max - x_min
        bbox_height = y_max - y_min
        bbox_size = max(bbox_width, bbox_height)

        # Skip masks that are smaller than 50 by 50 pixels
        if bbox_size < 50:
          continue

        # Add padding to include more context around the mask
        padded_size = bbox_size + padding
        x_center = (x_min + x_max) // 2
        y_center = (y_min + y_max) // 2

        # Ensure the bounding box is square and centered
        half_size = padded_size // 2
        x_min = max(0, x_center - half_size)
        y_min = max(0, y_center - half_size)
        x_max = min(raw_image.width, x_center + half_size)
        y_max = min(raw_image.height, y_center + half_size)

        # Crop the image around the padded bounding box
        cropped_image = raw_image.crop((x_min, y_min, x_max, y_max))

        # Convert the cropped image to a format that can be edited with PIL
        cropped_image_np = np.array(cropped_image)
        img_with_outline = Image.fromarray(cropped_image_np)

        segmented_images.append(img_with_outline)
        segmented_images_bboxes.append([x_min, y_min, x_max, y_max])

        # Create transparent segmented image
        transparent_img = Image.new("RGBA", cropped_image.size)
        cropped_image_rgba = cropped_image.convert("RGBA")
        mask_cropped = mask_np[y_min:y_max, x_min:x_max]
        mask_rgba = Image.fromarray((mask_cropped * 255).astype(np.uint8)).convert("L")
        transparent_img.paste(cropped_image_rgba, (0, 0), mask_rgba)
        transparent_segmented_images.append(transparent_img)
    
    if debug:
        # Save the segmented images with masks outlined
        for i, img in enumerate(segmented_images):
            if not os.path.exists("./images/segments"): 
                os.makedirs("./images/segments")
            img.save(f"./images/segments/segmented_{i}.png")

        # Save the transparent segmented images
        for i, img in enumerate(transparent_segmented_images):
            if not os.path.exists("./images/transparent_segments"): 
                os.makedirs("./images/transparent_segments")
            img.save(f"./images/transparent_segments/transparent_segmented_{i}.png")

    return segmented_images, segmented_images_bboxes, transparent_segmented_images
