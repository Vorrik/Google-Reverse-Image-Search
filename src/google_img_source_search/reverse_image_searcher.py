import re
from requests import Session

from .google_items.search_item import SearchItem
from .safe_modes import SafeMode
from .exceptions import SafeModeSwitchError

from .image_uploader import ImageUploader
from .image_file_uploader import ImageFileUploader
from .image_source_searcher import ImageSourceSearcher


class ReverseImageSearcher:
    def __init__(self, session=None, image_uploader=None, image_file_uploader=None, image_source_searcher=None):
        self.session = session or Session()
        self.image_uploader = image_uploader or ImageUploader(self.session)
        self.image_file_uploader = image_file_uploader or ImageFileUploader(self.session)
        self.image_source_searcher = image_source_searcher or ImageSourceSearcher(self.session)

        self.session.headers.update(
            {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        )
        self.session.hooks = {
            'response': lambda r, *args, **kwargs: r.raise_for_status()
        }

    def switch_safe_mode(self, safe_mode: SafeMode):
        safe_search_response = self.session.get('https://google.com/safesearch')

        switch_attr = {SafeMode.DISABLED: 'data-setprefs-off-url',
                       SafeMode.BLUR: 'data-setprefs-blur-url',
                       SafeMode.FILTER: 'data-setprefs-filter-url'}[safe_mode]

        switch_params = re.search(rf'(?<={switch_attr}=").*?(?=")', safe_search_response.text).group(0)
        switch_response = self.session.get(f'https://google.com{switch_params.replace("amp;", "")}')

        if switch_response.status_code != 204:
            raise SafeModeSwitchError()

    def __search(self, image_uploader: ImageUploader, image: str) -> list[SearchItem]:
        google_image = image_uploader.upload(image)
        return self.image_source_searcher.search(google_image)

    def search(self, image_url: str) -> list[SearchItem]:
        """
        Searches for web pages using the specified image. By image url
        :return: list of search items (page url, title, image url)
        """

        return self.__search(self.image_uploader, image_url)

    def search_by_file(self, image_path: str) -> list[SearchItem]:
        """
        Searches for web pages using the specified image. By image file path
        :return: list of search items (page url, title, image url)
        """

        return self.__search(self.image_file_uploader, image_path)
