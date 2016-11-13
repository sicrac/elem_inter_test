import django
from django.core.management import base
from django.utils import text, html
from image_data import models
from image_data import utils
import csv
import re
import io


class Command(base.BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            dest='url',
            help='Url of the csv data file. If no url is given, a default one will be used',
            type=str
        )
        parser.add_argument(
            '--preserve',
            action='store_true',
            dest='preserve',
            default=False,
            help='Preserve existing data',
        )

    def _notice(self, i, message):
        return self.style.NOTICE('ROW %s: %s' % (i, message))

    def _success(self, i, message):
        return self.style.SUCCESS('ROW %s: %s' % (i, message))

    @staticmethod
    def _fix_row(title, description, image_url):
        title = re.split('[,\n]', title)[0].strip()
        title = text.Truncator(title).chars(models.ImageData._meta.get_field('title').max_length)
        description = html.strip_tags(description.strip())
        image_url = image_url.strip()
        return title, description, image_url

    def handle(self, *args, **options):
        try:
            url = options['url'] or django.conf.settings.CSV_URL
            csv_fd = io.BytesIO(utils.download_file(url))
        except utils.DownloadError:
            raise base.CommandError("Invalid url: %s" % url)

        if not options['preserve']:
            for o in models.ImageData.objects.all():
                o.delete()

        csv_fd.next()
        for i, (title, description, image_url) in enumerate(csv.reader(csv_fd)):
            row_num = i + 1

            title, description, image_url = self._fix_row(title, description, image_url)

            if not title or not description:
                self.stderr.write(self._notice(row_num, 'skipped - empty title and/or description'))
                continue

            data_entry = models.ImageData(title=title, description=description)
            data_entry.save()

            if not image_url:
                self.stdout.write(self._notice(row_num, 'empty url'))
                continue

            try:
                data_entry.save(image_url)
            except utils.DownloadError as e:
                self.stdout.write(self._notice(row_num, e.message))
                continue
            else:
                self.stdout.write(self._success(row_num, 'downloaded url "%s"' % image_url))
