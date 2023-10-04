

import uuid


import os


BUCKET_NAME = 'item-exchange'
IMAGE_PREFIX = 'item-images'




#method to generate unique file name for image
def generate_unique_file_name():
    # Generate a unique file name.
    file_name = '{}/{}'.format(IMAGE_PREFIX, uuid.uuid4())
    # Return the file name.
    return file_name


#method to delete image from google cloud storage
def delete_image_from_gcs(file_name, bucket_name=BUCKET_NAME):
    # Get the bucket object.
    bucket = storage.Bucket(bucket_name)

    # Get the blob object.
    blob = bucket.blob(file_name)

    # Delete the image from Google Cloud Storage.
    blob.delete()


