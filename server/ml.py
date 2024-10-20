import torch
from torchvision import models, transforms
from PIL import Image
import chromadb
import os

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

    def load_image(img_path):
        """
        
        """
        image = Image.open(img_path).convert('RGB')
        return image

    def get_image_vector_embedding(img_path):
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

    def get_image_data(image):
        pass

    def get_image_list_data(list_of_images: list):
        """
        Given a list of images (tensors) returns a list of
        tuples where each tuple contains important data of the image

        returns Tuple[vectorEmbedding, name, desc, category]
        """
        pass

    def process_video(video):
        """
        Args
        - video: a video file of a room

        Return
        - String: response of successful video upload
        """
        pass