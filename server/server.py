from flask import Flask, request, jsonify
import sqlite3
import uuid
import json
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('items.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/item', methods=['POST'])
def create_item():
    data = request.json
    item_id = str(uuid.uuid4())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Items (id, name, description, category, images)
    VALUES (?, ?, ?, ?, ?)
    ''', (item_id, data['name'], data['description'], data['category'], json.dumps(data['images'])))
    conn.commit()
    conn.close()
    
    return jsonify({"id": item_id, "message": "Item created successfully"}), 201

@app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    item = cursor.execute('SELECT * FROM Items WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(dict(item))

@app.route('/upload_session', methods=['POST'])
def create_upload_session():
    data = request.json
    session_id = str(uuid.uuid4())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO UploadSession (id, date, after, items)
    VALUES (?, ?, ?, ?)
    ''', (session_id, datetime.now().isoformat(), data['after'], json.dumps(data['items'])))
    conn.commit()
    conn.close()
    
    return jsonify({"id": session_id, "message": "Upload session created successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)