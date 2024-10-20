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

    conn.commit()
    conn.close()

def set_item(name, description, category, price, item_id):
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

    cursor.execute('''
        INSERT OR REPLACE INTO Items (id, name, description, category, price, count)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (item_id, name, description, category, price, 1)) # sets count to 1

    conn.commit()
    conn.close()
    return item_id

def increment_item_count(item_id):
    """
    Increment the count of a given item by a specified amount.

    Args:
        item_id (str): The UUID of the item to increment.
        increment (int, optional): The amount to increment the count by. Defaults to 1.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    conn = open_connection()
    cursor = conn.cursor()

    try:
        # First, check if the item exists
        cursor.execute("SELECT count FROM Items WHERE id = ?", (item_id,))
        result = cursor.fetchone()

        if result is None:
            print(f"No item found with id: {item_id}")
            return False

        current_count = result[0]
        new_count = current_count + 1

        # Update the count
        cursor.execute('''
            UPDATE Items
            SET count = ?
            WHERE id = ?
        ''', (new_count, item_id))

        conn.commit()
        print(f"Item count updated. New count: {new_count}")
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()

def update_item(item_id, name, description, category, price):
    """
    Update an item in the Items table. If the item already exists, increment its count;
    if not, create a new item with the provided details.

    Args:
        name (str): The name of the item.
        description (str): The description of the item.
        category (str): The category of the item.
        price (str): The price of the item.
        count (int): The initial count of the item (used only if creating a new item).
        item_id (str): The UUID of the item.

    Returns:
        str: The UUID of the item.
    """
    conn = open_connection()
    cursor = conn.cursor()

    try:
        # Check if the item_id already exists
        cursor.execute("SELECT id FROM Items WHERE id = ?", (item_id,))
        result = cursor.fetchone()

        if result:
            # If the item exists, increment the count
            print(f"Item with ID {item_id} already exists. Incrementing count.")
            increment_item_count(item_id)
        else:
            # If the item doesn't exist, insert it with the provided details
            print(f"Item with ID {item_id} does not exist. Creating new item.")
            set_item(name, description, category, price, item_id)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

    return item_id

# Initialize the database when this module is imported
initialize_database()