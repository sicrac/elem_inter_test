from django.test import TestCase
import django

from PIL import Image
import mock
import os
import io

from image_data import models


class TestImageDate(TestCase):

    IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'image.jpeg')
    IMAGE_URL_MOCK = 'http://www.example.com/image.jpeg'

    @mock.patch('image_data.models.utils.download_image')
    def test_save(self, download_image_mock):
        try:
            download_image_mock.return_value = Image.open(io.BytesIO(open(self.IMAGE_PATH).read()))
            image_data = models.ImageData(title='title', description='Description')
            image_data.save(self.IMAGE_URL_MOCK)
            self.assertLessEqual(Image.open(image_data.image), django.conf.settings.IMAGE_SIZE)
            image_data.delete()
        finally:
            if os.path.isfile(image_data.image.path):
                os.remove(image_data.image.path)

    @mock.patch('image_data.models.utils.download_image')
    def test_delete(self, download_image_mock):
        try:
            download_image_mock.return_value = Image.open(self.IMAGE_PATH)
            image_data = models.ImageData(title='title', description='Description')
            image_data.save(self.IMAGE_URL_MOCK)
            self.assertTrue(os.path.isfile(image_data.image.path))
            image_data.delete()
            self.assertFalse(os.path.isfile(image_data.image.path))
        finally:
            if os.path.isfile(image_data.image.path):
                os.remove(image_data.image.path)

    def test_delete_without_image(self):
        image_data = models.ImageData(title='title', description='Description')
        image_data.save()
        image_data.delete()
