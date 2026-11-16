import os
import uuid
import base64

from imagekitio import ImageKit

imagekit = ImageKit(
    private_key=os.environ.get("IMAGEKIT_PRIVATE_KEY"),
    public_key=os.environ.get("IMAGEKIT_PUBLIC_KEY"),
    url_endpoint=os.environ.get("IMAGEKIT_URL_ENDPOINT"),
)
# https://docs.imagekit.io/api-reference/upload-file-api/server-side-file-upload
def upload_image(file):
    # Generate a unique filename for the avatar
    filename = str(uuid.uuid4())
    imgstr = base64.b64encode(file.read())
    response = imagekit.upload_file(imgstr, file_name=filename)
    print(response.url)
    # Return the URL of the uploaded avatar
    return response.url
