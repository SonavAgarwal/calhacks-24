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
from db import *

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
    before = request.args.get('before')

    print('upload_media')

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
        if file.content_type not in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/quicktime']:
            return jsonify({'error': 'Invalid file type'}), 400

        # TODO: send the files through the pipeline (call process_video or process_image)
        if file.content_type == 'video/mp4' or file.content_type == 'video/quicktime':
            print('processing video', file)
            uploads = process_video(file, s3, before)
        else:
            print('processing image', file)
            uploads = process_image(file, s3, before)
        
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
    
    # print("Filtered images", filtered_images)

    ids = filtered_images['ids'][0]
    metadatas = filtered_images['metadatas'][0]

    results = list(zip(ids, metadatas))

    print("looping through results")

    items = {}
    for id, metadata in results:
        print(f"Item ID: {id}, Metadata: {metadata}")
        # Get the item details from the image
        item_id = metadata.get('item_id')
        if not item_id:
            continue
        item_details = get_item(item_id)
        if item_details and item_details['id'] not in items:
            item_details['before_images'] = []
            item_details['after_images'] = []
            item_details['before_count'] = item_details.get('before_count', 0)
            item_details['after_count'] = item_details.get('after_count', 0)
            items[item_details['id']] = item_details

    print("BEFORE IMAGES ADDED TO ITEMS")
    # Print out the items
    for item in items.values():
        print(f"Item: {item}")

    # Now add the images to the items under the 'before_images' or 'after_images' key
    for id, metadata in results:
        print(f"Adding image to item {id}")
        item_obj = items.get(metadata.get('item_id', None), None)
        if item_obj:
            if metadata.get('before', True):  # Assuming 'before' is True by default
                item_obj['before_images'].append(metadata)
                item_obj['before_count'] += 1
            else:
                item_obj['after_images'].append(metadata)
                item_obj['after_count'] += 1

    print("AFTER IMAGES ADDED TO ITEMS")
    # print out the items
    for item in items.values():
        print(f"Item: {item}")

    # convert the items dict to a list
    items = list(items.values())

    # for id, metadata in results:

    # returns all the items in the inventory, joined with their images
    return jsonify({"items": items}), 200


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
# Set pending images to done

@app.route('/set_pending_to_done', methods=['POST'])
def set_pending_to_done():
    data = request.json

    result = filter_images_by_metadata(status='pending')
    image_ids = result['ids'] 
    for id in image_ids:
        update_image_status(id, new_status='done')

    return jsonify({"message": f"Images {image_ids} updated from 'pending' to 'done' status"}), 200



###################
# Accept images to inventory

@app.route('/accept_to_inventory', methods=['POST'])
def accept_to_inventory():
    data = request.json
    image_ids = data['image_ids']
    print(f"Accepting images to inventory: {image_ids}")

    for image_id in image_ids:
        # update the status of the image to 'inventory'
        update_image_status(image_id, 'inventory')

    return jsonify({"message": "Images accepted to inventory successfully"}), 200

@app.route('/delete_from_inventory', methods=['POST'])
def delete_from_inventory():
    data = request.json
    item_id = data['item_id']
    print(f"Deleting images from inventory: {item_id}")

    delete_images_by_item_id(item_id)

    return jsonify({"message": "Images deleted from inventory successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5003)
