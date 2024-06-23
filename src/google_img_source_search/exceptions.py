class GoogleImageSearcherError(Exception):
    pass


class InvalidImageURL(GoogleImageSearcherError):
    pass


class SafeModeSwitchError(GoogleImageSearcherError):
    pass
