import os
from image_data import utils
from django.test import TestCase
import requests_mock
import io
import PIL
import re


class TestDownloadImage(TestCase):

    IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'image.jpeg')
    IMAGE_URL_MOCK = 'http://www.example.com/image.jpeg'

    def test(self):
        with requests_mock.mock() as server_mock, open(self.IMAGE_PATH) as image:
            content = image.read()
            matcher = server_mock.get(self.IMAGE_URL_MOCK, content=content)
            image_file = utils.download_image(self.IMAGE_URL_MOCK)
            self.assertTrue(matcher.called_once)
            self.assertEqual(matcher.last_request._request.method, 'GET')
            self.assertEqual(matcher.last_request._request.url, self.IMAGE_URL_MOCK)
            self.assertEqual(PIL.Image.open(io.BytesIO(content)), image_file)

    def test_invalid_images(self):
        with requests_mock.mock() as server_mock, open(self.IMAGE_PATH) as image:
            content = image.read()[::-1]
            matcher = server_mock.get(self.IMAGE_URL_MOCK, content=content)
            self.assertRaisesRegexp(
                utils.DownloadError,
                re.escape('url "http://www.example.com/image.jpeg" does not point to a valid image'),
                utils.download_image, self.IMAGE_URL_MOCK)
            self.assertTrue(matcher.called_once)
            self.assertEqual(matcher.last_request._request.method, 'GET')
            self.assertEqual(matcher.last_request._request.url, self.IMAGE_URL_MOCK)

    def test_not_found(self):
        with requests_mock.mock() as server_mock:
            matcher = server_mock.get(self.IMAGE_URL_MOCK, status_code=522, reason='Any Reason')
            self.assertRaisesRegexp(
                utils.DownloadError,
                re.escape('url "http://www.example.com/image.jpeg" is not correct (522 - Any Reason)'),
                utils.download_image, self.IMAGE_URL_MOCK)
            self.assertTrue(matcher.called_once)
            self.assertEqual(matcher.last_request._request.method, 'GET')
            self.assertEqual(matcher.last_request._request.url, self.IMAGE_URL_MOCK)

    def test_not_existent(self):
        self.assertRaisesRegexp(
            utils.DownloadError,
            re.escape('url "http://www.notexistentdomain.com/image.jpeg" does not exists'),
            utils.download_image, 'http://www.notexistentdomain.com/image.jpeg')


