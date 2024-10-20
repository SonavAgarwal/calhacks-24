import sqlite3
import uuid

def generate_uuid():
    """Generate a new UUID."""
    return str(uuid.uuid4())

def open_connection():
    """Open a connection to the SQLite database."""
    return sqlite3.connect('items_and_images.db')

def initialize_database():
    """Initialize the database by creating necessary tables."""
    conn = open_connection()
    cursor = conn.cursor()

    # Create Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            price TEXT,
            count INTEGER
        )
    ''')

    # Create Image Metadata Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Images (
            id TEXT PRIMARY KEY,
            item_id TEXT NOT NULL,
            after BOOLEAN NOT NULL,
            FOREIGN KEY (item_id) REFERENCES Items (id)
        )
    ''')

    # Create Upload Session Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UploadSession (
            id TEXT PRIMARY KEY,
            image_id TEXT NOT NULL,
            processing BOOLEAN NOT NULL,
            after BOOLEAN NOT NULL,
            FOREIGN KEY (image_id) REFERENCES Images (id)
        )
    ''')

    conn.commit()
    conn.close()

def set_item(name, description, category, price, count, item_id=None):
    """
    Set or update an item in the Items table.

    Args:
        name (str): The name of the item.
        description (str): The description of the item.
        category (str): The category of the item.
        price (str): The price of the item.
        count (int): The count of the item.
        item_id (str, optional): The UUID of the item. If not provided, a new UUID will be generated.

    Returns:
        str: The UUID of the item (either the provided one or a newly generated one).
    """
    conn = open_connection()
    cursor = conn.cursor()

    if item_id is None:
        item_id = generate_uuid()

    cursor.execute('''
        INSERT OR REPLACE INTO Items (id, name, description, category, price, count)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (item_id, name, description, category, price, count))

    conn.commit()
    conn.close()
    return item_id

def set_image(item_id, is_after, image_id=None):
    """
    Set an image associated with an item in the Images table.
    
    Args:
        item_id (str): The UUID of the item the image is associated with.
        is_after (bool): Whether the image is an 'after' image (True) or a 'before' image (False).
        image_id (str, optional): The UUID for the image. If not provided, a new UUID will be generated.
    
    Returns:
        str: The UUID of the image (either the provided one or a newly generated one).
    """
    conn = open_connection()
    cursor = conn.cursor()

    if image_id is None:
        image_id = generate_uuid()

    cursor.execute('''
        INSERT OR REPLACE INTO Images (id, item_id, after)
        VALUES (?, ?, ?)
    ''', (image_id, item_id, is_after))

    conn.commit()
    conn.close()
    return image_id

def add_upload_session(image_ids, after):
    """
    Add a new upload session for multiple images.

    Args:
        image_ids (list): List of image UUIDs to be included in the upload session.
        after (bool): Whether these are 'after' images (True) or 'before' images (False).

    Returns:
        str: The UUID of the newly created upload session.
    """
    conn = open_connection()
    cursor = conn.cursor()

    upload_session_id = generate_uuid()

    for image_id in image_ids:
        cursor.execute('''
            INSERT INTO UploadSession (id, image_id, processing, after)
            VALUES (?, ?, ?, ?)
        ''', (upload_session_id, image_id, True, after))

    conn.commit()
    conn.close()
    return upload_session_id

def upload_session_complete(upload_session_id):
    """
    Mark a given upload session as complete by setting its processing status to False.
    
    Args:
        upload_session_id (str): The UUID of the upload session to mark as complete.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    conn = open_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE UploadSession
            SET processing = ?
            WHERE id = ?
        ''', (False, upload_session_id))

        if cursor.rowcount == 0:
            print(f"No upload session found with id: {upload_session_id}")
            return False

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()

# Initialize the database when this module is imported
initialize_database()