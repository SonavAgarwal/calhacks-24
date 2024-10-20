import sqlite3
import uuid
from datetime import datetime

# Function to create the UUID
def generate_uuid():
    return str(uuid.uuid4())

# Connect to SQLite database (or create it)
conn = sqlite3.connect('items_and_images.db')
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
        after BOOLEAN NOT NULL,
        processing BOOLEAN NOT NULL,
        items TEXT -- Storing item-image mapping as a JSON string for simplicity
    )
''')

conn.commit()

# add methods

# Close the connection
conn.close()
