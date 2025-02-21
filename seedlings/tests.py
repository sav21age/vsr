from urllib.parse import urlencode
from django.test import TestCase, Client
from django.urls import reverse


APP = 'seedlings'


class SeedlingsProductTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_listview(self):
        """ Test ListView """
        response = self.client.get(reverse(f"{APP}:list"))
        self.assertEqual(response.status_code, 200)

        kwargs = {
            'division': 1,
            'per_page': 12,
            'page': 1
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

    def test_listview_filter_division(self):
        """ Test ListView with division """
        lst = [1, '1.5', '1,5', '1¾', 'test', None, '']
        for value in lst:
            kwargs = {'division': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 200)

        lst = [100000,]
        for value in lst:
            kwargs = {'division': value}
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

        lst = [100000000, 'test', ]
        for value in lst:
            kwargs = {'page': value}
            response = self.client.get('{0}?{1}'.format(
                reverse(f"{APP}:list"), urlencode(kwargs)))
            self.assertEqual(response.status_code, 404)
