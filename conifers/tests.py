from urllib.parse import urlencode
from django.test import TestCase, Client
from django.urls import reverse
from conifers.models import ConiferProduct


APP = 'conifers'


class ConiferProductTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """

        obj = ConiferProduct.is_visible_objects \
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

    def test_listview_filters(self):
        """ Test ListView with filters"""
        url = reverse(f"{APP}:list")

        genus = species = 1

        kwargs = {'genus': genus, }
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 200)

        kwargs = {'genus': 'genus', }
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 404)

        kwargs = {'genus': '⅓', }
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 404)

        kwargs = {'genus': 1000,}
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 404)

        kwargs = {'genus': genus, 'per_page': 1000}
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 200)

        kwargs = {'genus': genus, 'per_page': 1000, 'page': 1000}
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 404)

        kwargs = {'genus': genus, 'species': species}
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 200)

        kwargs = {'genus': genus, 'species': '⅓'}
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 404)

        kwargs = {'genus': '⅓', 'species': '3'}
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 404)

        kwargs = {'genus': genus, 'species': species,
                  'per_page': 1000, 'page': 1000}
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 404)

        kwargs = {'genus': genus, 'species': 2}
        response = self.client.get(f"{url}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 404)

    def test_listview_per_page(self):
        """ Test ListView with per_page """
        per_page = [8, 12, 24, 36, 'test', None, '']

        for value in per_page:
            kwargs = {'per_page': value}
            response = self.client.get('{0}?{1}'.format(reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

    def test_listview_pagination(self):
        """ Test ListView with pagination """

        page = (1,)
        for value in page:
            kwargs = {'page': value}
            response = self.client.get('{0}?{1}'.format(reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

        page = (100000000, 'test')
        for value in page:
            kwargs = {'page': value}
            response = self.client.get('{0}?{1}'.format(reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 404)