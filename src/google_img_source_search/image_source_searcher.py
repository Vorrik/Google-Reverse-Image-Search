from requests import Session

from .google_items.search_item import SearchItem
from .batchexecute_decoder import decode
from .f_req_template import build_f_req
from .google_items.image import Image


class ImageSourceSearcher:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def extract_search_items(src_response: str) -> list[SearchItem]:
        """ Extracts image sources """

        decoded_response = decode(src_response, 'c')
        if len(decoded_response[0][2][1][0][1][8]) < 21:
            return []  # No images found error

        return [SearchItem(page_url=search_item[2][2][2], page_title=search_item[1][0], image_url=search_item[0][0])
                for search_item in decoded_response[0][2][1][0][1][8][20][0][0]]

    def search(self, image: Image) -> list[SearchItem]:
        params = {
            'soc-app': '1',
            'soc-platform': '1',
            'soc-device': '1',
            'rt': 'c'
        }

        data = {
            'f.req': build_f_req(image.id_1, image.id_2)
        }

        src_response = self.session.post('https://lens.google.com/_/LensWebStandaloneUi/data/batchexecute',
                                         params=params, data=data, allow_redirects=True)

        return self.extract_search_items(src_response.text)
