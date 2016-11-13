import os

from django.core.management import call_command
from django.test import TestCase
from image_data import models

import mock
import PIL


class CommandsTestCase(TestCase):

    IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'image.jpeg')
    CSV_PATH = os.path.join(os.path.dirname(__file__), 'data.csv')

    def tearDown(self):
        for o in models.ImageData.objects.all():
            o.delete()

    @mock.patch('image_data.utils.download_file')
    @mock.patch('image_data.utils.download_image')
    def test_load_csv(self, download_image_mock, download_file_mock):
        content = open(self.CSV_PATH).read()
        download_file_mock.return_value = content
        download_image_mock.return_value = PIL.Image.open(open(self.IMAGE_PATH))

        args = []
        options = {'url': 'http://www.example.com/data.csv'}
        call_command('load_csv', *args, **options)
        download_file_mock.assert_called_once_with(options['url'])

        self.assertItemsEqual(
            [mock.call('http://www.example.com/image1.jpg'),
             mock.call('http://www.example.com/image2.jpg'),
             mock.call('http://www.example.com/image3.jpg')],
            download_image_mock.call_args_list)

        self.assertEqual(models.ImageData.objects.count(), 3)

    @mock.patch('image_data.utils.download_file')
    @mock.patch('image_data.utils.download_image')
    def test_load_csv_with_preserve(self, download_image_mock, download_file_mock):
        content = open(self.CSV_PATH).read()
        download_file_mock.return_value = content
        download_image_mock.return_value = PIL.Image.open(open(self.IMAGE_PATH))

        args = []
        options = {'url': 'http://www.example.com/data.csv'}
        call_command('load_csv', *args, **options)
        download_file_mock.assert_called_once_with(options['url'])

        self.assertItemsEqual(
            [mock.call('http://www.example.com/image1.jpg'),
             mock.call('http://www.example.com/image2.jpg'),
             mock.call('http://www.example.com/image3.jpg')],
            download_image_mock.call_args_list)

        self.assertEqual(models.ImageData.objects.count(), 3)

        args = ['--preserve']
        call_command('load_csv', *args, **options)
        download_file_mock.assert_has_calls([mock.call(options['url']), mock.call(options['url'])])

        self.assertItemsEqual(
            [mock.call('http://www.example.com/image1.jpg'),
             mock.call('http://www.example.com/image2.jpg'),
             mock.call('http://www.example.com/image3.jpg'),
             mock.call('http://www.example.com/image1.jpg'),
             mock.call('http://www.example.com/image2.jpg'),
             mock.call('http://www.example.com/image3.jpg')],
            download_image_mock.call_args_list)

        self.assertEqual(models.ImageData.objects.count(), 6)
