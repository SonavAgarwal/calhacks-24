import torch
from torchvision import models, transforms
from PIL.Image import Image, open
from typing import List
from chromadb.utils import embedding_functions

# Check for GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# # Load pre-trained ResNet50 model
# embedding_model = models.resnet50(pretrained=True)

# EMBEDDING_DIM_SIZE = embedding_model.fc.in_features
# print('EMBEDDING_DIM_SIZE', EMBEDDING_DIM_SIZE)

# embedding_model = torch.nn.Sequential(*list(embedding_model.children())[:-1])  # Remove the last fully connected layer
# embedding_model = embedding_model.to(device)
# embedding_model.eval()

# # Define image preprocessing
# preprocess = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
# ])

default_ef = embedding_functions.DefaultEmbeddingFunction()
EMBEDDING_DIM_SIZE = len(default_ef(["test"])[0])

# def get_image_vector_embedding(image: Image):
#         """
#         Creates a vector embedding of an image using
#         ResNet50 model with the output layer removed.

#         Args
#         - img_path: img_path of image

#         Return
#         - vector embedding tensor
#         """
#         # Load and preprocess the image
#         image = image.convert('RGB')
#         img_tensor = preprocess(image)
#         img_tensor = img_tensor.unsqueeze(0).to(device)  # Add batch dimension and move to GPU
        
#         # Generate the embedding
#         with torch.no_grad():
#             features = embedding_model(img_tensor)
        
#         return features.cpu().squeeze().numpy()

def get_image_description_vector_embedding(name: str):
    """
    Creates a vector embedding of an image name using
    chromadb like below:
    from chromadb.utils import embedding_functions
    """

    return default_ef([name])
