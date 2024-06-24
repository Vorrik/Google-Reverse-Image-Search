import os
import mimetypes

from .image_uploader import ImageUploader
from .exceptions import InvalidOrUnsupportedImageFile
from .google_items.image import Image


class ImageFileUploader(ImageUploader):

    def upload(self, image_path: str) -> Image:
        image_file = open(image_path, 'rb')
        multipart = {'encoded_image': (os.path.basename(image_path), image_file, mimetypes.guess_type(image_path)[0])}
        upload_response = self.session.post('https://lens.google.com/v3/upload', files=multipart)
        image_file.close()

        if "{'ds:0'" not in upload_response.text:
            raise InvalidOrUnsupportedImageFile()

        return self.extract_image(upload_response.text)
