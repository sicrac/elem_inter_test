import requests
import io
from PIL import Image


class DownloadError(Exception):
    """ Custom exception raised by `download_image` """


def download_file(file_url):
    """
    Downloads the image pointed by `file_url`.
    It may raises a `DownloadError` in case of a not existing url, a `Not Found` error returned by the server.

    :param file_url: [str]
    :return: [subclasses of PIL.ImageFile.ImageFile]
    """
    try:
        r = requests.get(file_url)
    except requests.exceptions.ConnectionError:
        raise DownloadError('url "%s" does not exists' % file_url)
    if not r.ok:
        raise DownloadError('url "%s" is not correct (%s - %s)' % (file_url, r.status_code, r.reason))
    return r.content


def download_image(image_url):
    """
    Downloads the image pointed by `image_url`.
    It may raises a `DownloadError` in case the downloaded file is not an image and because of `download_file`.

    :param image_url: [str]
    :return: [subclasses of PIL.ImageFile.ImageFile]
    """
    content = download_file(image_url)
    try:
        return Image.open(io.BytesIO(content))
    except IOError:
        raise DownloadError('url "%s" does not point to a valid image' % image_url)
