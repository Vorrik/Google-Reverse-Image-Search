from requests import Session

from .google_items.image import Image
from .google_items.search_item import SearchItem
from .f_req_template import build_f_req
from .api_response_parser import ApiResponseParser


class ReverseImageSearcher:
    def __init__(self):
        self.url = 'https://lens.google.com'
        self.session = Session()
        self.session.headers.update(
            {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        )
        self.session.hooks = {
            'response': lambda r, *args, **kwargs: r.raise_for_status()
        }

    def upload_image(self, image_url: str) -> Image:
        upload_response = self.session.get(f'{self.url}/uploadbyurl', params={'url': image_url}, allow_redirects=True)
        return ApiResponseParser.extract_image(upload_response.text)

    def search_image_src(self, image: Image) -> list[SearchItem]:
        params = {
            'soc-app': '1',
            'soc-platform': '1',
            'soc-device': '1',
            'rt': 'c',
        }

        data = {
            'f.req': build_f_req(image.id_1, image.id_2)
        }

        src_response = self.session.post(f'{self.url}/_/LensWebStandaloneUi/data/batchexecute',
                                         params=params, data=data, allow_redirects=True)

        return ApiResponseParser.extract_image_src(src_response.text)

    def search(self, image_url: str) -> list[SearchItem]:
        """
        Searches for image sources by URL using google services
        :return: list of search items
        """

        google_image = self.upload_image(image_url)
        return self.search_image_src(google_image)
