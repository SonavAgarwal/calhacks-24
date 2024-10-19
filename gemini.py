import cv2
import base64
import json
import numpy as np
import vertexai
import math
from vertexai.generative_models import GenerativeModel, Part

vertexai.init(project="mpi2instances-350406", location="us-west4")
model = GenerativeModel("gemini-1.5-flash-001")

# Function to encode image to base64
def load_image_and_encode_base64(image) -> str:
    _, buffer = cv2.imencode('.jpg', image)
    image_bytes = buffer.tobytes()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    return encoded_image

# Function to call Gemini model and get GPT response
def get_gpt_response(base64str) -> str:
    image_part = Part.from_data(mime_type="image/jpeg", data=base64.b64decode(base64str))
    
    text1 = """
    You will be finding a maximum of 20 different items/objects/furniture in this image (except wall structure and people), including their estimated monetary value and pixel bounding box in the image. For each item found, you must ensure the following:
    1. **If there are multiple of the same item**, list them under a single key with an appropriate quantity and bounding boxes.
    2. **Do not duplicate item names.** Use only one key per item type.
    3. Each item's value and bounding boxes must be represented as strings.
    4. The output format must **strictly follow JSON formatting rules**, with keys as strings, like the following example:
    ```json
    {"item_name":{"quantity":"", "cost_per_item":"", "bounding_boxes":[{"x1":,"x2":,"y1":,"y2":},...]}}
    ```
    5. **Important**: The JSON should be a single object containing each item as a key. Ensure there are no duplicate keys. Do not output anything other than the JSON object itself.
    Start the JSON output here:"""
    
    generation_config = {"max_output_tokens": 8192, "temperature": 1, "top_p": 0.95}

    responses = model.generate_content([image_part, text1], generation_config=generation_config, stream=True)
    gptoutput = "".join([response.text for response in list(responses)]).replace('json','').replace('```','')
    return gptoutput

# Function to split the panorama into square images
def split_image_into_squares(image, square_size):
    height, width, _ = image.shape
    square_images = []
    positions = []

    # Sliding window approach to extract squares
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            square = image[y:y+square_size, x:x+square_size]
            square_images.append(square)
            positions.append((x, y))  # Store the position of the top-left corner of each square

    return square_images, positions

# Function to adjust bounding boxes to original panorama dimensions
def adjust_bounding_boxes(items_data, position, square_size, original_width, original_height):
    adjusted_items = {}

    for item_name, item_info in items_data.items():
        if item_name not in adjusted_items:
            adjusted_items[item_name] = {"quantity": item_info["quantity"], "cost_per_item": item_info["cost_per_item"], "bounding_boxes": []}
        
        for bbox in item_info["bounding_boxes"]:
            # Adjust the bounding box coordinates
            x1 = int(bbox["x1"]) / 1000.0 * square_size + position[0]
            y1 = int(bbox["y1"]) / 1000.0 * square_size + position[1]
            x2 = int(bbox["x2"]) / 1000.0 * square_size + position[0]
            y2 = int(bbox["y2"]) / 1000.0 * square_size + position[1]
            
            # Ensure bounding boxes do not exceed the original panorama dimensions
            x1 = min(original_width, max(0, x1))
            y1 = min(original_height, max(0, y1))
            x2 = min(original_width, max(0, x2))
            y2 = min(original_height, max(0, y2))
            
            adjusted_items[item_name]["bounding_boxes"].append({"x1": str(x1), "x2": str(x2), "y1": str(y1), "y2": str(y2)})

    return adjusted_items

# Function to process the panorama image
def process_panorama(image_path, square_size):
    # Load the panorama image
    panorama = cv2.imread(image_path)

    # Get original image dimensions
    original_height, original_width, _ = panorama.shape

    # Split the panorama into squares
    square_images, positions = split_image_into_squares(panorama, square_size)

    # Loop through each square image, get GPT response and adjust bounding boxes
    final_output = {}

    for i, square_image in enumerate(square_images):
        position = positions[i]

        # Encode square image and get response from Gemini
        base64_str = load_image_and_encode_base64(square_image)
        gpt_response = get_gpt_response(base64_str)
        
        # Convert GPT response to JSON and adjust bounding boxes
        try:
            items_data = json.loads(gpt_response)
            adjusted_items = adjust_bounding_boxes(items_data, position, square_size, original_width, original_height)
            
            # Merge results into final output
            for item_name, item_info in adjusted_items.items():
                if item_name not in final_output:
                    final_output[item_name] = {"quantity": item_info["quantity"], "cost_per_item": item_info["cost_per_item"], "bounding_boxes": []}
                
                final_output[item_name]["bounding_boxes"].extend(item_info["bounding_boxes"])

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response for square {i}: {e}")

    return final_output

def find_optimal_square_size(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Get image dimensions
    height, width, _ = image.shape
    
    # Find the greatest common divisor (GCD) of height and width
    optimal_square_size = math.gcd(height, width)
    
    print(f"Optimal square size to maximize space: {optimal_square_size}x{optimal_square_size}")
    return optimal_square_size


# Function to display bounding boxes on the final image
def display_image_with_bboxes(json_data, image_path):
    items_data = json.loads(json_data)

    # Load the original panorama image
    image = cv2.imread(image_path)

    # Get image dimensions
    shape1, shape2, _ = image.shape  # shape1 is height, shape2 is width

    # Loop through items and plot bounding boxes
    for item_name in items_data:
        for bbox in items_data[item_name]["bounding_boxes"]:
            
            # Extract the bounding box coordinates
            x1, y1 = int(bbox["x1"]), int(bbox["y1"])
            x2, y2 = int(bbox["x2"]), int(bbox["y2"])

            print(f"Bounding box: {item_name} (({x1}, {y1}), ({x2}, {y2})))")

            # Draw the rectangle for each bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box
            
            # Put label (item name) on the image
            cv2.putText(image, item_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Save the image with bounding boxes and labels
    cv2.imwrite("boxes_with_borders.jpg", image)


# Example usage
panorama_path = "pan1.png"
square_size = find_optimal_square_size(panorama_path)

json_output = process_panorama(panorama_path, square_size)
display_image_with_bboxes(json.dumps(json_output), panorama_path)