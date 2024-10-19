import torch
from torchvision import models, transforms
from PIL import Image
import chromadb
import os

# Check for GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load pre-trained ResNet50 model
model = models.resnet50(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])  # Remove the last fully connected layer
model = model.to(device)
model.eval()

# Define image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
    
# Initialize ChromaDB client
client = chromadb.Client()

# Create or get a collection
collection = client.create_collection("image_vectors")

def vectorize_image(img_path):
    # Load and preprocess the image
    image = Image.open(img_path).convert('RGB')
    img_tensor = preprocess(image)
    img_tensor = img_tensor.unsqueeze(0).to(device)  # Add batch dimension and move to GPU
    
    # Generate the embedding
    with torch.no_grad():
        features = model(img_tensor)
    
    return features.cpu().squeeze().numpy()

def add_images_to_collection(image_folder):
    for i, filename in enumerate(os.listdir(image_folder)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            img_path = os.path.join(image_folder, filename)
            vector = vectorize_image(img_path)
            collection.add(
                embeddings=[vector.tolist()],
                documents=[filename],
                ids=[f"img_{i+1}"]
            )
    print(f"Added {i+1} images to the collection.")

def find_nearest_image(query_img_path):
    # Vectorize the query image
    query_vector = vectorize_image(query_img_path)
    
    # Query ChromaDB for the nearest vector
    results = collection.query(
        query_embeddings=[query_vector.tolist()],
        n_results=1
    )
    
    return results

if __name__ == "__main__":
    # Add images to the collection
    image_folder = "images\embd"
    add_images_to_collection(image_folder)

    # Find the nearest match for a query image
    query_image_path = "images\\test.jpg"
    nearest_match = find_nearest_image(query_image_path)
    
    print("Nearest match:")
    print(nearest_match)
    # print(f"ID: {nearest_match['ids'][0][0]}")
    # print(f"Image: {nearest_match['documents'][0][0]}")
    # print(f"Distance: {nearest_match['distances'][0][0]}")