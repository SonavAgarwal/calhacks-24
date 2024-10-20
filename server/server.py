# import boto3
# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# import uuid
# import json
# from datetime import datetime
# # from db import get_db_connection
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# app.config['CORS_HEADERS'] = 'Content-Type'


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


# # @app.route('/item', methods=['POST'])
# # def create_item():
# #     data = request.json
# #     item_id = str(uuid.uuid4())

# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     cursor.execute('''
# #     INSERT INTO Items (id, name, description, category, images)
# #     VALUES (?, ?, ?, ?, ?)
# #     ''', (item_id, data['name'], data['description'], data['category'], json.dumps(data['images'])))
# #     conn.commit()
# #     conn.close()

# #     return jsonify({"id": item_id, "message": "Item created successfully"}), 201


# # @app.route('/item/<item_id>', methods=['GET'])
# # def get_item(item_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     item = cursor.execute(
# #         'SELECT * FROM Items WHERE id = ?', (item_id,)).fetchone()
# #     conn.close()

# #     if item is None:
# #         return jsonify({"error": "Item not found"}), 404

# #     return jsonify(dict(item))


# # @app.route('/upload_session', methods=['POST'])
# # def create_upload_session():
# #     data = request.json
# #     session_id = str(uuid.uuid4())

# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     cursor.execute('''
# #     INSERT INTO UploadSession (id, date, after, items)
# #     VALUES (?, ?, ?, ?)
# #     ''', (session_id, datetime.now().isoformat(), data['after'], json.dumps(data['items'])))
# #     conn.commit()
# #     conn.close()

# #     return jsonify({"id": session_id, "message": "Upload session created successfully"}), 201


# @app.route('/upload_images', methods=['POST'])
# def upload_images():

#     print("Hello")
#     return jsonify({'image_urls': ['http']}), 200
#     # print(request.files)

#     # S3_BUCKET = 'calhacks-images'

#     # # Create a new S3 client
#     # s3 = boto3.client('s3')

#     # # Get the uploaded file from the request
#     # if 'files[]' not in request.files:
#     #     return jsonify({'error': 'No image files provided'}), 400

#     # files = request.files.getlist('files[]')
#     # print(files)
#     # if len(files) == 0:
#     #     return jsonify({'error': 'No image files provided'}), 400

#     # uploaded_images = []

#     # for file in files:

#     #     # Generate a unique image ID
#     #     image_id = str(uuid.uuid4())

#     #     # Secure the file name
#     #     filename = secure_filename(file.filename)
#     #     file_extension = filename.split('.')[-1]

#     #     # Create the S3 object key
#     #     s3_key = f"{image_id}.{file_extension}"

#     #     # Upload the image to S3
#     #     try:
#     #         s3.upload_fileobj(
#     #             file,
#     #             S3_BUCKET,
#     #             s3_key,
#     #             # Make the file publicly accessible
#     #             ExtraArgs={'ACL': 'public-read'}
#     #         )
#     #     except Exception as e:
#     #         return jsonify({'error': str(e)}), 500


#     #     # Construct the image URL
#     #     image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"
#     #     uploaded_images.append(image_url)
#     # # Return the image URL
#     # return jsonify({'image_urls': uploaded_images}), 200
# if __name__ == '__main__':
#     app.run(debug=True, host='localhost', port=5000)

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all origins by default
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
