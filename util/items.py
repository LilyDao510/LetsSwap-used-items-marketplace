import uuid
import base64

from imagekitio import ImageKit

imagekit = ImageKit(
    private_key='private_y6pDCa9EuxN3UZRp/oGqKNvyVC0=',
    public_key='public_34Jp1/QR0bWgSkoZotQv03GONZk=',
    url_endpoint='https://ik.imagekit.io/jkpzdliog/item-exchange-images'
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
