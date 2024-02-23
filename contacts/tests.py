from django.test import TestCase, Client
from django.urls import reverse
from contacts.models import Contacts


class ContactPageTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_detail(self):
        """ Test contacts detail view """

        obj = Contacts.objects.get()
        response = self.client.get(reverse(obj.slug))
        self.assertEqual(response.status_code, 200)

    def test_detail_not_exists(self):
        """ Test contacts detail view not exists """

        self.assertRaises(Contacts.DoesNotExist, Contacts.objects.get, slug='anything')
