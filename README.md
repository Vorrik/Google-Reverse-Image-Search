# Google Reverse Image Search
[![PyPI version](https://badge.fury.io/py/google-image-source-search.svg)](https://badge.fury.io/py/google-image-source-search)

An unofficial simple solution to search web pages using the specified image. Written on pure requests

![Google lens](https://raw.githubusercontent.com/Vorrik/Google-Image-Source-Search/master/examples/google_lens0.png)

## Installation
```sh
> pip install google-image-source-search
```

## Usage
```py
from google_img_source_search import ReverseImageSearcher


if __name__ == '__main__':
    image_url = 'https://i.pinimg.com/originals/c4/50/35/c450352ac6ea8645ead206721673e8fb.png'

    rev_img_searcher = ReverseImageSearcher()
    res = rev_img_searcher.search(image_url)

    for search_item in res:
        print(f'Title: {search_item.page_title}')
        print(f'Site: {search_item.page_url}')
        print(f'Img: {search_item.image_url}\n')
```
#### Switching safe mode
```py
from google_img_source_search import SafeMode
rev_img_searcher.switch_safe_mode(SafeMode.DISABLED)
```
#### Passing custom session
```py
import requests
session = requests.Session()
rev_img_searcher = ReverseImageSearcher(session)
```

### Results
#### Output:
```
Title: WAIFU OR LAIFU? - YouTube
Site: https://www.youtube.com/watch?v=F8l5OgLpuyM
Img: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKg0oMfWeMyBo0-KRerecMaRXNLI2zTLqmyXc0TgDS7nWJx3aB

Title: Печальный факт о Эмилии из аниме "Re:Zero. Жизнь с нуля в альтернативном мире" | AniGAM | Дзен
Site: https://dzen.ru/a/ZBs3vFvEYSvIxPhv
Img: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTA-RDMY-xUrV5Qqn5fYjJ9qFsZC2Posk16qHkWh4sdnVP5Leh7

Title: Stream chocho music | Listen to songs, albums, playlists for free on SoundCloud
Site: https://soundcloud.com/chocho-329200480
Img: https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQycLi6Ug9JtqKp5t6irb-3Pbj26DtTT48P-R38lOqVI5pXCwYz
```
#### Google lens:
![Google lens](https://raw.githubusercontent.com/Vorrik/Google-Image-Source-Search/master/examples/google_lens.png)
