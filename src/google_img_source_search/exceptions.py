class GoogleImageSearcherError(Exception):
    pass


class ImageUploadError(GoogleImageSearcherError):
    pass


class InvalidImageURL(ImageUploadError):
    pass


class InvalidOrUnsupportedImageFile(ImageUploadError):
    pass


class SafeModeSwitchError(GoogleImageSearcherError):
    pass
