from PIL import Image
import chromadb
import numpy as np
import uuid
from image_embedding import EMBEDDING_DIM_SIZE

def generate_uuid():
    """Generate a new UUID."""
    return str(uuid.uuid4())

# Initialize ChromaDB client
client = chromadb.HttpClient(host='18.225.156.100', port=8000)

# Create or get a collection
collection = client.create_collection("image_vectors", get_or_create=True)

def add_image_vector_to_collection(vector_embedding, url_path, before: bool, status: str):
    """
    Add a vector embedding along with metadata to the ChromaDB collection.
    
    Args:
        vector_embedding (np.ndarray): The vector embedding of the image.
        url_path (str): The URL path of the image.
        before (bool): A flag indicating if it's a 'before' image.
        status (str): The status of the image (e.g., 'processed', 'pending').
    
    Return:
        image_id: image_id of the new uploaded image
        item_id: id of the item associated with image
    """

    image_id = generate_uuid()
    item_id = get_item_uuid_of_embedding(vector_embedding)

    metadata = {
        "image_id": image_id,
        "item_id": item_id,
        "url_path": url_path,
        "before": before,
        "status": status
    }

    # Add the vector embedding along with metadata to the collection
    collection.add(
        embeddings=[vector_embedding.tolist()],  # Ensure vector_embedding is converted to list
        documents=[url_path],  # Typically a document is the reference (e.g., image URL)
        ids=[image_id],  # Use the UUID as the unique identifier
        metadatas=[metadata]  # Add metadata for this entry
    )

    print(f"Added image with item_id {item_id} and URL {url_path} to the collection.")
    return image_id, item_id


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

def find_nearest_image(vector_embedding):
    "Return the nearest image to the given embedding"
    return find_k_nearest_images(vector_embedding, k=1)

def get_item_uuid_of_embedding(vector_embedding, distance_threshold=400):
    """
    Get the item UUID of an embedding if there's a similar one within the distance threshold,
    otherwise generate a new UUID.
    
    Args:
    vector_embedding (np.ndarray): The vector embedding to check.
    distance_threshold (float): The maximum distance to consider embeddings as similar.
    
    Returns:
    str: The UUID of the similar embedding or a new UUID.
    """
    # Query for the nearest embedding
    results = find_k_nearest_images(vector_embedding, k=1)
    
    if results and 'distances' in results and results['distances']:
        
        if len(results['distances'][0]) == 0:
            # No similar embedding found
            return generate_uuid()

        nearest_distance = results['distances'][0][0]  # Assuming 'distances' is a list of lists, take the first element
        
        if nearest_distance <= distance_threshold:
            # Return the item ID of the nearest embedding if it's within the threshold
            return results['ids'][0][0]
    
    # If no similar embedding found or distance is above threshold, generate a new UUID
    return generate_uuid()

def filter_images_by_metadata(item_id=None, url_path=None, before=None, status=None, num_results=100):
    """
    Filter the ChromaDB collection based on metadata fields.
    
    Args:
        item_id (str, optional): The UUID of the associated item. Default is None.
        url_path (str, optional): The URL path of the image. Default is None.
        before (bool, optional): A flag indicating if it's a 'before' image. Default is None.
        status (str, optional): The status of the image (e.g., 'processed', 'pending'). Default is None.
        num_results (int, optional): The max number of images that will be returned. Default is 100.

    Returns:
        dict: The filtered results from the ChromaDB collection.
    """
    # Build the filter dictionary based on the provided metadata
    filter_conditions = {}
    
    if item_id is not None:
        filter_conditions['item_id'] = item_id
    if url_path is not None:
        filter_conditions['url_path'] = url_path
    if before is not None:
        filter_conditions['before'] = before
    if status is not None:
        filter_conditions['status'] = status

    # Perform the query with the constructed filter
    results = collection.query(
        query_embeddings=[0]*EMBEDDING_DIM_SIZE,  # Empty because we are only filtering by metadata, not by vector
        where=filter_conditions,  # Apply the filter conditions
        n_results=num_results  # Set to a reasonable number; adjust based on your needs
    )
    
    return results

def update_image_status(image_id, new_status):
    """
    Update the status of an image with the given image_id in the ChromaDB collection.
    
    Args:
        image_id (str): The UUID of the image to update.
        new_status (str): The new status to set for the image.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        # First, we need to get the current metadata for the image
        results = collection.get(
            ids=[image_id],
            include=['metadatas']
        )

        if not results['metadatas']:
            print(f"No image found with id: {image_id}")
            return False

        # Get the current metadata
        current_metadata = results['metadatas'][0]

        # Update the status in the metadata
        current_metadata['status'] = new_status

        # Update the image in the collection with the new metadata
        collection.update(
            ids=[image_id],
            metadatas=[current_metadata]
        )

        print(f"Successfully updated status of image {image_id} to {new_status}")
        return True

    except Exception as e:
        print(f"An error occurred while updating image status: {str(e)}")
        return False