from __future__ import unicode_literals

import django
from django.db import models
from django.core import files

from PIL import Image
import io

from image_data import utils

image_storage = files.storage.FileSystemStorage('media/images')


class ImageData(models.Model):

    title = models.CharField(max_length=20)
    description = models.CharField(max_length=120, blank=True)
    image = models.ImageField(storage=image_storage)

    def save(self, image_url=None, image_file=None, **kw):
        super(ImageData, self).save(**kw)

        if not image_url and not image_file:
            return

        if image_url:
            image_file = utils.download_image(image_url)

        buff = io.BytesIO()
        image_file.thumbnail(django.conf.settings.IMAGE_SIZE, Image.ANTIALIAS)
        image_file.save(buff, format=image_file.format)

        self.image.save("%s.%s" % (self.id, image_file.format.lower()), files.base.ContentFile(buff.getvalue()))
        super(ImageData, self).save(**kw)

    def delete(self, **kw):
        storage = self.image.storage
        path = self.image.path if hasattr(self.image, 'path') else None
        super(ImageData, self).delete(**kw)
        if path:
            storage.delete(path)
