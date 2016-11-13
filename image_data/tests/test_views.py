import urllib
import os
from PIL import Image

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from image_data import models


class BaseTest(APITestCase):

    IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'image.jpeg')
    URL_NAME = None

    def tearDown(self):
        for o in models.ImageData.objects.all():
            o.delete()

    @classmethod
    def url(cls, qs=None, reverse_kwargs=None):
        if not qs:
            return reverse(cls.URL_NAME, kwargs=reverse_kwargs)
        return '%s?%s' % (reverse(cls.URL_NAME, kwargs=reverse_kwargs), urllib.urlencode(qs))

    @classmethod
    def create(cls, n):
        for i in range(1, n + 1):
            o = models.ImageData(title='Title %s' % i, description='Description %s' % i)
            image_file = Image.open(cls.IMAGE_PATH)
            o.save(image_file=image_file)


class IndexTests(BaseTest):

    URL_NAME = 'index'

    def test(self):
        self.create(10)
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(10, len(json_response))

    def test_empty(self):
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(0, len(json_response))

    def test_with_search_matches_title(self):
        self.create(10)
        response = self.client.get(self.url(qs=dict(search='Title 1')))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(2, len(json_response))
        self.assertItemsEqual(['Title 1', 'Title 10'], [o['title'] for o in json_response])

    def test_with_search_matches_description(self):
        self.create(10)
        response = self.client.get(self.url(qs=dict(search='Description 1')))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(2, len(json_response))
        self.assertItemsEqual(['Description 1', 'Description 10'], [o['description'] for o in json_response])

    def test_with_search_matches_title_and_description(self):
        self.create(10)
        o = models.ImageData(title='Title abc', description='Description')
        o.save()
        o = models.ImageData(title='Title', description='Description abc')
        o.save()
        response = self.client.get(self.url(qs=dict(search='1')))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(2, len(json_response))

    def test_with_search_empty(self):
        self.create(10)
        response = self.client.get(self.url(qs=dict(search='XXXXXX')))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(0, len(json_response))


class ImageRawTests(BaseTest):

    URL_NAME = 'image-raw'

    def test(self):
        self.create(10)
        response = self.client.get(self.url(reverse_kwargs=dict(pk=8)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('content-type'), 'image/jpeg')

    def test_not_found(self):
        response = self.client.get(self.url(reverse_kwargs=dict(pk=8)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_found_image(self):
        o = models.ImageData(title='title', description='description')
        o.save()
        response = self.client.get(self.url(reverse_kwargs=dict(pk=o.id)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
