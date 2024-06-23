from dataclasses import dataclass


@dataclass
class SearchItem:
    page_url: str
    page_title: str
    image_url: str
