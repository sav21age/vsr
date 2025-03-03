from urllib.parse import urlencode

from django.test import Client, TestCase
from django.urls import reverse

from roses.models import RoseProduct


APP = 'roses'


class RoseProductTest(TestCase):
    fixtures = [
        'fixtures/plants.json',
        'fixtures/roses.json', 
    ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """

        obj = RoseProduct.is_visible_objects \
            .prefetch_related('images') \
            .all()[:1].get()

        response = self.client.get(
            reverse(f"{APP}:detail", kwargs={'slug': obj.slug}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse(f"{APP}:detail", kwargs={'slug': 'anything'}))
        self.assertEqual(response.status_code, 404)

    def test_listview(self):
        """ Test ListView """
        response = self.client.get(reverse(f"{APP}:list"))
        self.assertEqual(response.status_code, 200)

        kwargs = {
            'species': 1, 
            'per_page': 12, 
            'page': 2
        }
        response = self.client.get('{0}?{1}'.format(
            reverse(f"{APP}:list"), urlencode(kwargs)))
        self.assertEqual(response.status_code, 200)

        kwargs.update({'page': 200, })
        response = self.client.get('{0}?{1}'.format(
            reverse(f"{APP}:list"), urlencode(kwargs)))
        self.assertEqual(response.status_code, 404)

    def test_listview_per_page(self):
        """ Test ListView with per_page """
        lst = [8, 12, 24, 36, 'test', None, '']

        for value in lst:
            kwargs = {'per_page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

    def test_listview_filter_species(self):
        """ Test ListView with species """
        lst = [1, '1.5', '1,5', '1¾', 'test', None, '']
        for value in lst:
            kwargs = {'species': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

        lst = [100000,]
        for value in lst:
            kwargs = {'species': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 404)

    def test_listview_pagination(self):
        """ Test ListView with pagination """

        lst = [1,]
        for value in lst:
            kwargs = {'page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

        lst = [100000000, 'test']
        for value in lst:
            kwargs = {'page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 404)
