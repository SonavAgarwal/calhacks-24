import torch
from torchvision import models, transforms
from PIL.Image import Image, open
import chromadb
import os
from typing import List
import hyperbolic

# Check for GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load pre-trained ResNet50 model
embedding_model = models.resnet50(pretrained=True)
embedding_model = torch.nn.Sequential(*list(embedding_model.children())[:-1])  # Remove the last fully connected layer
embedding_model = embedding_model.to(device)
embedding_model.eval()

# Define image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

class Processing:
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

    def get_image_vector_embedding(image: Image):
        """
        Creates a vector embedding of an image using
        ResNet50 model with the output layer removed.

        Args
        - img_path: img_path of image

        Return
        - vector embedding tensor
        """
        # Load and preprocess the image
        img_tensor = preprocess(image)
        img_tensor = img_tensor.unsqueeze(0).to(device)  # Add batch dimension and move to GPU
        
        # Generate the embedding
        with torch.no_grad():
            features = embedding_model(img_tensor)
        
        return features.cpu().squeeze().numpy()

    def get_image_data(image: Image):
        """
        Given an Image, returns a tuple of all the image data

        Returns:
        - (vectorEmbedding, name, desc, category)
        """

        vector_embedding = Processing.get_image_vector_embedding(image)

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
            img_data = Processing.get_image_data(image)
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

        # 7.1) upload

        pass