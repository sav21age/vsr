from django.test import TestCase, Client, override_settings
from django.urls import reverse
from contacts.models import Contacts, WorkSchedule


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


class WorkScheduleTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.client = Client()

    def test_work_schedule(self):
        """ Test contacts change work schedule """
        with override_settings(CACHE_TIMEOUT=900):
            obj = WorkSchedule.objects.get()
            obj.name = 'CLOSED'
            obj.save()
            response = self.client.get(reverse('index'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Закрыт до весны')

            obj.name = 'NORMAL'
            obj.save()
            response = self.client.get(reverse('index'))
            self.assertContains(
                response, 'Пн-Сб: 09:00-19:00, Вс: <span class="text-danger fw-bold">выходной</span>', html=True)


