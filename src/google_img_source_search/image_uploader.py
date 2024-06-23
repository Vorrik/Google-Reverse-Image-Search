import re
import json
from requests import Session

from .exceptions import InvalidImageURL
from .google_items.image import Image


class ImageUploader:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def extract_image(upload_response: str) -> Image:
        """ Extracts image object from upload response """

        js_obj = re.search(r'(?<=AF_dataServiceRequests = ).*?(?=; var)', upload_response).group(0)
        py_obj = json.loads(re.sub(r'([{\s,])(\w+)(:)', r'\1"\2"\3', js_obj.replace("'", '"')))

        id_1 = py_obj['ds:0']['request'][0][0]
        id_2 = py_obj['ds:0']['request'][1][7][0]

        return Image(id_1, id_2)

    def upload(self, image_url: str) -> Image:
        upload_response = self.session.get('https://lens.google.com/uploadbyurl', params={'url': image_url})

        if "{'ds:0'" not in upload_response.text:
            raise InvalidImageURL()

        return self.extract_image(upload_response.text)
