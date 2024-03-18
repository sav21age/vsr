from django.test import TestCase, Client
from search.forms import SearchForm


class SearchFormTest(TestCase):
    """
     Test search form
    """

    def test_empty_fields(self):
        form_data = {'q': ''}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_q_is_one_char(self):
        form_data = {'q': 'A'}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_q_is_valid(self):
        form_data = {'q': 'роза'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class SearchPageTest(TestCase):

    fixtures = ['fixtures/db.json',]

    def setUp(self):
        self.client = Client()

    def test_search_pages(self):
        """
         Test search pages
        """
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/search/?q=')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/search/?q=роза')
        self.assertEqual(response.status_code, 200)
