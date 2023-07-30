import json
import _jsonnet

from .google_items.image import Image
from .google_items.search_item import SearchItem
from .batchexecute_decoder import decode


class ApiResponseParser:

    @staticmethod
    def extract_image(upload_response: str) -> Image:
        """ Extracts image object from upload response """

        try:
            start_index = upload_response.index("{'ds:0'")
            end_index = upload_response.index("; var AF_initDataChunkQueue")
            js_obj = upload_response[start_index:end_index]
            py_obj = json.loads(_jsonnet.evaluate_snippet('snippet', js_obj))

            id_1 = py_obj['ds:0']['request'][0][0]
            id_2 = py_obj['ds:0']['request'][1][7][0]

            return Image(id_1, id_2)
        except ValueError:
            raise RuntimeError('Invalid image url')

    @staticmethod
    def extract_image_src(src_response: str) -> list[SearchItem]:
        """ Final image src response parsing """

        decoded_response = decode(src_response, 'c')
        image_sources = []
        try:
            for search_item in decoded_response[0][2][1][0][1][8][20][0][0]:
                image_sources.append(SearchItem(
                    page_url=search_item[2][2][2],
                    page_title=search_item[1][0],
                    image_url=search_item[0][0]
                ))
        except IndexError:
            # No results
            pass

        return image_sources
