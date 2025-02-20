from urllib.parse import urlencode
from django.test import TestCase, Client
from django.urls import reverse
from conifers.forms import ConiferProductPriceFilterForm
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

    def test_listview_filter_form(self):
        """ Test ListView filter form """

        form_data = {
            'genus': [1,],
            'height_from': 70,
            'extra': 'on',
        }

        form = ConiferProductPriceFilterForm(data=form_data)
        # print(form.errors)
        self.assertTrue(form.is_valid())

        response = self.client.get(
            reverse(f"{APP}:list"), data=form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(form['genus'].value(), [1])
        self.assertEqual(form['height_from'].value(), 70)
        self.assertEqual(form['extra'].value(), True)
        
    def test_listview_filter_form_xhr_valid(self):
        """ Test ListView filter form XMLHttpRequest valid """

        json_data = {
            'genus': [1,],
            'height_from': 70,
            'extra': 'on',
        }

        response = self.client.post(reverse(f"{APP}:filter_form"), json_data)
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            reverse(f"{APP}:filter_form"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        # json_response = '{"genus": [1, 12], "height_from": {"min": 70, "max": 240}, "width_from": {"min": null, "max": null}, "container": [3], "rs": [1], "shtamb": null, "extra": []}'
        json_response = '{"genus": [1, 9, 12], "height_from": {"min": 100, "max": 280}, "width_from": {"min": null, "max": null}, "container": [], "rs": [1], "shtamb": null, "extra": []}'
        self.assertEqual(response.content.decode('utf-8'), json_response)
        
    def test_listview_filter_form_xhr_not_valid(self):
        """ Test ListView filter form XMLHttpRequest not valid """

        json_data = {
            'genus': 'test',
            'height_from': 'test',
            'extra': 'on',
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

    # def test_listview(self):
    #     """ Test ListView """
    #     url = reverse(f"{APP}:list")

    #     genus = species = 1

    #     kwargs = {'genus': genus, }
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 200)

    #     kwargs = {'genus': 'genus', }
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 404)

    #     kwargs = {'genus': '⅓', }
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 404)

    #     kwargs = {'genus': 1000,}
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 404)

    #     kwargs = {'genus': genus, 'per_page': 1000}
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 200)

    #     kwargs = {'genus': genus, 'per_page': 1000, 'page': 1000}
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 404)

    #     kwargs = {'genus': genus, 'species': species}
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 200)

    #     kwargs = {'genus': genus, 'species': '⅓'}
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 404)

    #     kwargs = {'genus': '⅓', 'species': '3'}
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 404)

    #     kwargs = {'genus': genus, 'species': species,
    #               'per_page': 1000, 'page': 1000}
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 404)

    #     kwargs = {'genus': genus, 'species': 2}
    #     response = self.client.get(f"{url}?{urlencode(kwargs)}")
    #     self.assertEqual(response.status_code, 404)
