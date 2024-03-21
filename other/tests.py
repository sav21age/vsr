from django.test import TestCase, Client
from django.urls import reverse
from other.models import OtherProduct


class RelatedProductTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """

        obj = OtherProduct.is_visible_objects.filter(category__name='RELATED') \
            .prefetch_related('images') \
            .all()[:1].get()

        response = self.client.get(
            reverse("related_detail", kwargs={'slug': obj.slug}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse("related_detail", kwargs={'slug': 'anything'}))
        self.assertEqual(response.status_code, 404)

    def test_listview(self):
        """ Test ListView """
        response = self.client.get(reverse("related_list"))
        self.assertEqual(response.status_code, 200)


class BookProductTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_detailview(self):
        """ Test DetailView """

        obj = OtherProduct.is_visible_objects.filter(category__name='BOOK') \
            .prefetch_related('images') \
            .all()[:1].get()

        response = self.client.get(
            reverse("book_detail", kwargs={'slug': obj.slug}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse("book_detail", kwargs={'slug': 'anything'}))
        self.assertEqual(response.status_code, 404)

    def test_listview(self):
        """ Test ListView """
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)