from django.test import TestCase, Client
from django.urls import reverse
from django.http import SimpleCookie
from adverts.models import Advert


class AdvertTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_advert(self):
        """ Test advert """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "advertContainer")

        try:
            advert = Advert.objects.get()
        except:
            body = "Далеко-далеко за словесными горами в стране гласных и согласных живут рыбные тексты. Вдали от всех живут они в буквенных домах."
            advert = Advert(
                title="Рыбный текст", body=body)
            advert.save()

        self.client.cookies = SimpleCookie({'advert_id': advert.id})
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, "advertContainer")

        self.client.cookies = SimpleCookie(
            {'advert_id': 'aa999a99-1030-489e-a08a-80684123a61e'})
        response = self.client.get(reverse('index'))
        self.assertContains(response, "advertContainer")

        # self.assertContains(
        #     self.response, '<h1>admin_docs.Person</h1>', html=True)
