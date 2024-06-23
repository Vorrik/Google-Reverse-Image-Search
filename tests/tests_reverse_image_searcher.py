import unittest
from src.google_img_source_search.reverse_image_searcher import ReverseImageSearcher, SafeMode


class TestReverseImageSearcher(unittest.TestCase):

    def setUp(self):
        self.reverse_image_searcher = ReverseImageSearcher()

    def test_search(self):
        results = self.reverse_image_searcher.search('https://i.pinimg.com/originals/c4/50/35'
                                                     '/c450352ac6ea8645ead206721673e8fb.png')
        self.assertTrue(results, 'No results')

    def test_switch_safe_mode(self):
        self.reverse_image_searcher.switch_safe_mode(SafeMode.DISABLED)
        self.reverse_image_searcher.switch_safe_mode(SafeMode.BLUR)
        self.reverse_image_searcher.switch_safe_mode(SafeMode.FILTER)
