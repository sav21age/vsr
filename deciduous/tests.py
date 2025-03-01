from urllib.parse import urlencode
from django.test import TestCase, Client
from django.urls import reverse
from deciduous.forms import DecProductPriceFilterForm
from deciduous.models import DecProduct


APP = 'deciduous'


class DecProductTest(TestCase):
    fixtures = [
        'fixtures/plants.json', 
        'fixtures/deciduous.json', 
    ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """

        obj = DecProduct.is_visible_objects \
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
            'genus': [64,],
            'height_from': 90,
            'container': 6,
        }

        form = DecProductPriceFilterForm(data=form_data)
        # print(form.errors)
        self.assertTrue(form.is_valid())

        response = self.client.get(
            reverse(f"{APP}:list"), data=form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(form['genus'].value(), [64,])
        self.assertEqual(form['height_from'].value(), 90)
        self.assertEqual(form['container'].value(), 6)

    def test_listview_filter_form_xhr_valid(self):
        """ Test ListView filter form XMLHttpRequest valid"""

        json_data = {
            'genus': [64,],
            'height_from': 90,
            'container': 6,
        }

        response = self.client.post(reverse(f"{APP}:filter_form"), json_data)
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            reverse(f"{APP}:filter_form"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        # json_response = '{"genus": [27, 35, 39, 63, 64, 66, 69, 72, 77, 80, 23, 85, 90], "height_from": {"min": 125, "max": 150}, "container": [6], "rs": [1], "shtamb": null, "extra": null}'
        json_response = '{"genus": [35, 39, 63, 64, 66, 69, 77, 80, 23, 85, 90], "height_from": {"min": 125, "max": 150}, "container": [6], "rs": [1], "shtamb": null, "extra": null}'
        self.assertEqual(response.content.decode('utf-8'), json_response)

    def test_listview_filter_form_xhr_not_valid(self):
        """ Test ListView filter form XMLHttpRequest not valid"""

        json_data = {
            'genus': 'test',
            'height_from': 'test',
            'container': 'test',
        }

        response = self.client.post(
            reverse(f"{APP}:filter_form"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '{}')


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
