import google.cloud import storage


#method to get image from google cloud storage with bucket name and file name
def get_image_from_gcs(bucket_name, file_name):
    # Get the bucket object.
    bucket = storage.Bucket(bucket_name)

    # Get the blob object.
    blob = bucket.blob(file_name)

    # Get the image object.
    image = blob.open('rb')
    return image

