from urllib.parse import urlencode
from django.test import TestCase, Client
from django.urls import reverse
from fruits.forms import FruitProductPriceFilterForm
from fruits.models import FruitProduct


APP = 'fruits'


class FruitProductTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """

        obj = FruitProduct.is_visible_objects \
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
            'genus': [36,],
            'container': 11,
        }

        form = FruitProductPriceFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

        response = self.client.get(
            reverse(f"{APP}:list"), data=form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(form['genus'].value(), [36])
        self.assertEqual(form['container'].value(), 11)

    def test_listview_filter_form_xhr(self):
        """ Test ListView filter form XMLHttpRequest """

        json_data = {
            'genus': [36,],
            'container': 11,
        }

        response = self.client.post(
            reverse(f"{APP}:filter_form"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        # json_response = '{"genus": [36, 40, 47, 50, 51], "container": [6, 11, 9], "rs": [], "age": [5]}'
        json_response = '{"genus": [36, 40, 47, 51], "container": [6, 11, 31, 9], "rs": [], "age": [5]}'
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
