import json
# import env
import os
import uuid
from datetime import datetime

import boto3
from aws import open_s3_client, upload_image_to_s3
from chroma import *
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from ml import process_image, process_video
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def hello_world():
    return 'Hello, World!'


###################
# Upload media

@app.route('/upload_media', methods=['POST'])
def upload_media():

    # Create a new S3 client
    s3 = open_s3_client()

    if s3 is None:
        return jsonify({'error': 'Could not initialize S3 client'}), 500

    # Get the uploaded file from the request
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files[]')
    if len(files) == 0:
        return jsonify({'error': 'No files provided'}), 400

    uploaded_images = []

    for file in files:

        # ensure the file is an image or video
        if file.content_type not in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4']:
            return jsonify({'error': 'Invalid file type'}), 400

        # TODO: send the files through the pipeline (call process_video or process_image)
        if file.content_type == 'video/mp4' or file.content_type == 'video/quicktime':
            uploads = process_video(file, s3)
        else:
            uploads = process_image(file, s3)

        uploaded_images += uploads

    # # Return the image URLs
    # return jsonify({'urls': uploaded_images}), 200
    return jsonify({'message': 'Media uploaded successfully'}), 200


###################
# Get the inventory

@app.route('/inventory', methods=['GET'])
def get_items():
    # do something to get inventory

    # metadata to filter by
    item_id = None
    url_path = None
    before = request.args.get('before')
    status = request.args.get('status')

    filtered_images = filter_images_by_metadata(
        item_id, url_path, before, status)

    for image in filtered_images:
        print(image)

    # returns all the items in the inventory, joined with their images
    return jsonify({"message": "Inventory fetched successfully"}), 200


###################
# Get pending uploads

@app.route('/pending_uploads', methods=['GET'])
def get_pending_uploads():
    # do something to get pending uploads
    filtered_images = filter_images_by_metadata(status='pending')

    pending_items = set()
    for image in filtered_images:
        image['']

    # TODO: return all the images that are pending upload (not yet in inventory)
    return jsonify({"message": "Pending uploads fetched successfully"}), 200


###################
# Accept images to inventory

@app.route('/accept_to_inventory', methods=['POST'])
def accept_to_inventory():
    data = request.json
    image_ids = data['image_ids']

    # do something with image_ids

    return jsonify({"message": "Images accepted to inventory successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)
