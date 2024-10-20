import sqlite3
import uuid
from datetime import datetime

# Function to create the UUID
def generate_uuid():
    return str(uuid.uuid4())

# Function to open a connection
def open_connection():
    return sqlite3.connect('items_and_images.db')

# Connect to SQLite database (or create it)
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
        after BOOLEAN NOT NULL,
        FOREIGN KEY (item_id) REFERENCES Items (id)
    )
''')

# Create Upload Session Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS UploadSession (
        id TEXT PRIMARY KEY,
        processing BOOLEAN NOT NULL,
        FOREIGN KEY (image_id) REFERENCES Images (id)
        after BOOLEAN NOT NULL
    )
''')

conn.commit()

# Close the connection
conn.close()


"""
METHODS
"""

# Add item to Items table
def set_item(name, description, category, price, count, item_id=None):
    """
    Sets item associated to a uuid to a certain value. This either
    updates an existing table entry or adds a new one. If no uuid
    is specified, a new entry is created. Otherwise it updates an
    existing item with the given uuid.
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

def set_image(is_after, item_id, image_id=None):
    """
    Sets an image associated with an item in the Images table.
    
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