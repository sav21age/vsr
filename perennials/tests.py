from urllib.parse import urlencode
from django.test import TestCase, Client
from django.urls import reverse
from perennials.forms import PerProductPriceFilterForm
from perennials.models import PerProduct


APP = 'perennials'


class PerProductTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """

        obj = PerProduct.is_visible_objects \
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

    def test_listview_filter_form(self):
        """ Test ListView filter form """

        form_data = {
            'genus': [21,],
            'container': 11,
            'planting_year': 2022,
        }

        form = PerProductPriceFilterForm(data=form_data)
        # print(form.errors)
        self.assertTrue(form.is_valid())

        response = self.client.get(
            reverse(f"{APP}:list"), data=form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(form['genus'].value(), [21,])
        self.assertEqual(form['container'].value(), 11)
        self.assertEqual(form['planting_year'].value(), 2022)

    def test_listview_filter_form_xhr(self):
        """ Test ListView filter form XMLHttpRequest """

        json_data = {
            'genus': [21,],
            'container': 11,
            'planting_year': 2022,
        }

        response = self.client.post(
            reverse(f"{APP}:filter_form"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        # json_response = '{"genus": [21], "container": [11, 19], "planting_year": [2022, 2023]}'
        json_response = '{"genus": [21], "container": [11, 3], "planting_year": [2022, 2023]}'
        self.assertEqual(response.content.decode('utf-8'), json_response)

    def test_listview_per_page(self):
        """ Test ListView with per_page """
        per_page = [8, 12, 24, 36, 'test', None, '']

        for value in per_page:
            kwargs = {'per_page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

    def test_listview_pagination(self):
        """ Test ListView with pagination """

        page = (1,)
        for value in page:
            kwargs = {'page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

        page = (100000000, 'test')
        for value in page:
            kwargs = {'page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 404)
