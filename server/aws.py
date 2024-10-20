import os
import uuid
import boto3
from flask import jsonify
from werkzeug.utils import secure_filename


def open_s3_client():

    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv(
                              'AWS_SECRET_ACCESS_KEY'),
                          region_name=os.getenv('AWS_DEFAULT_REGION')

                          )
        return s3
    except Exception as e:
        print(f"Error initializing S3 client: {e}")
        return None


def upload_image_to_s3(s3connection, file):
    s3 = s3connection
    S3_BUCKET = 'calhacks-images'

    # Generate a unique image ID
    image_id = str(uuid.uuid4())

    # Secure the file name
    filename = secure_filename(file.filename)
    file_extension = filename.split('.')[-1]

    # Create the S3 object key
    s3_key = f"{image_id}.{file_extension}"

    # Upload the image to S3
    try:
        print(f"Uploading {filename} as {s3_key} to S3...")
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            s3_key,
            ExtraArgs={'ACL': 'public-read'}
        )
        print(f"Upload successful for {s3_key}")

        image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"
        return image_url

    except Exception as e:
        print(f"Error uploading file {filename}: {e}")
        return None
