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

    # Create Items Table with before_count and after_count
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            price TEXT,
            before_count INTEGER,
            after_count INTEGER
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
        item_id (str, optional): The UUID of the item. If not provided, a new UUID will be generated.

    Returns:
        str: The UUID of the item (either the provided one or a newly generated one).
    """
    conn = open_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO Items (id, name, description, category, price, before_count, after_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (item_id, name, description, category, price, 1, 0))  # sets before_count to 1 and after_count to 0

    conn.commit()
    conn.close()
    return item_id

def increment_item_count(item_id, before=True):
    """
    Increment the before_count or after_count of a given item by 1.

    Args:
        item_id (str): The UUID of the item to increment.
        before (bool, optional): If True, increment before_count, otherwise increment after_count. Defaults to True.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    conn = open_connection()
    cursor = conn.cursor()

    try:
        # First, check if the item exists
        cursor.execute("SELECT before_count, after_count FROM Items WHERE id = ?", (item_id,))
        result = cursor.fetchone()

        if result is None:
            print(f"No item found with id: {item_id}")
            return False

        before_count, after_count = result

        if before:
            new_count = before_count + 1
            cursor.execute('''
                UPDATE Items
                SET before_count = ?
                WHERE id = ?
            ''', (new_count, item_id))
            print(f"Item before_count updated. New count: {new_count}")
        else:
            new_count = after_count + 1
            cursor.execute('''
                UPDATE Items
                SET after_count = ?
                WHERE id = ?
            ''', (new_count, item_id))
            print(f"Item after_count updated. New count: {new_count}")

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()

def update_item(item_id, name, description, category, price, before=True):
    """
    Update an item in the Items table. If the item already exists, increment its before_count or after_count;
    if not, create a new item with the provided details.

    Args:
        name (str): The name of the item.
        description (str): The description of the item.
        category (str): The category of the item.
        price (str): The price of the item.
        item_id (str): The UUID of the item.
        before (bool, optional): If True, increment before_count, otherwise increment after_count. Defaults to True.

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
            # If the item exists, increment the appropriate count
            print(f"Item with ID {item_id} already exists. Incrementing {'before' if before else 'after'} count.")
            increment_item_count(item_id, before)
        else:
            # If the item doesn't exist, insert it with the provided details
            print(f"Item with ID {item_id} does not exist. Creating new item.")
            set_item(name, description, category, price, item_id)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

    return item_id

def get_item(item_id):
    """
    Retrieve an item from the Items table by its UUID.

    Args:
      item_id (str): The UUID of the item to retrieve.

    Returns:
      dict: A dictionary containing the item's details, or None if the item does not exist.
    """
    conn = open_connection()
    cursor = conn.cursor()

    print(f"Retrieving item with ID: {item_id}")

    try:
        cursor.execute("SELECT * FROM Items WHERE id = ?", (item_id,))
        result = cursor.fetchone()

        if result:
            item = {
                'id': result[0],
                'name': result[1],
                'description': result[2],
                'category': result[3],
                'price': result[4],
                'before_count': result[5],
                'after_count': result[6]
            }
            return item
        else:
            print(f"No item found with id: {item_id}")
            return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

def remove_item(item_id):
    try:
        conn = open_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Items WHERE id = ?", (item_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Item {item_id} removed from SQLite database")
            return True
        else:
            print(f"No item found with id {item_id} in SQLite database")
            return False
    except Exception as e:
        print(f"Error removing item {item_id} from SQLite database: {str(e)}")
        return False
    finally:
        conn.close()

# Initialize the database when this module is imported
initialize_database()