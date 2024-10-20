import torch
from torchvision import models, transforms
from PIL import Image
import chromadb
import os

# Initialize ChromaDB client
client = chromadb.HttpClient(host='18.225.156.100', port=8000)

# Create or get a collection
collection = client.create_collection("image_vectors")

def add_image_vector_to_collection(img_path, vector_embedding):
    collection.add(
        embeddings=[vector_embedding],
        documents=[img_path],
        ids=[img_path]
    )
    print(f"Added {img_path} to the collection.")

def find_k_nearest_images(vector_embedding, k):
    """
    Given a vector embedding of an image finds the k nearest vector embeddings
    """
    
    # Query ChromaDB for the nearest vector
    results = collection.query(
        query_embeddings=[vector_embedding.tolist()],
        n_results=k
    )
    
    return results
