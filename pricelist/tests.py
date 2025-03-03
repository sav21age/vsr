from django.test import Client, TestCase
from django.urls import reverse

from pricelist.templatetags.filename import get_filename
from pricelist.templatetags.filesize import get_filesize


class PriceDetailTest(TestCase):
    fixtures = ['fixtures/pricelist.json', ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """
        response = self.client.get(reverse('price_list_detail'))
        self.assertEqual(response.status_code, 200)


class PriceDetailTestNotExists(TestCase):
    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """
        response = self.client.get(reverse('price_list_detail'))
        self.assertEqual(response.status_code, 404)


class FileSizeTemplateFilterTest(TestCase):
    def test_get_filesize(self):
        self.assertEqual(get_filesize(111), '111 Б')
        self.assertEqual(get_filesize(2222), '2 КБ')
        self.assertEqual(get_filesize(33333), '33 КБ')
        self.assertEqual(get_filesize(444444), '434 КБ')
        self.assertEqual(get_filesize(5555555), '5.3 МБ')
        self.assertEqual(get_filesize(6666666666), '6.2 ГБ')
        self.assertEqual(get_filesize(-111), '0 Б')
        self.assertEqual(get_filesize('test'), '0 Б')


class FileNameTemplateFilterTest(TestCase):
    def test_get_filename(self):
        path = '/file/name/template/filter/file.zip'
        self.assertEqual(get_filename(path), 'file.zip')

        path = '/file/name/template/filter/file/zip'
        self.assertEqual(get_filename(path), 'zip')

        path = None
        self.assertEqual(get_filename(path), '')

        path = ''
        self.assertEqual(get_filename(path), '')
