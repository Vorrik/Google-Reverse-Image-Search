from src.google_img_source_search import ReverseImageSearcher

image_path = r"C:\Users\ammar\Downloads\61yHqiEtKRL.jpg"
rev_img_searcher = ReverseImageSearcher()
res = rev_img_searcher.search(image_path)

for search_item in res:
    print(f'Title: {search_item.page_title}')
    print(f'Site: {search_item.page_url}')
    print(f'Img: {search_item.image_url}\n')
