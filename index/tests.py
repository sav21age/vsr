from django.test import TestCase, Client
from django.urls import reverse

from conifers.models import ConiferProduct
from deciduous.models import DecProduct
from fruits.models import FruitProduct
from index.models import Index
from perennials.models import PerProduct


class IndexTest(TestCase):
    fixtures = ['fixtures/index.json', ]

    def setUp(self):
        self.client = Client()

    def test_index(self):
        """ Test index """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_content(self):
        """ Test content """

        caption = 'Хвойные – благородные растения, которые позволяют саду оставаться привлекательным и зеленым круглый год'
        response = self.client.get(reverse('index'))
        self.assertContains(response, caption)

        ConiferProduct.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, caption)

        #--

        caption = 'Лиственные деревья и кустарники – это обычно растения с черешковыми пластинчатыми листьями'
        response = self.client.get(reverse('index'))
        self.assertContains(response, caption)

        DecProduct.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, caption)

        #--

        caption = 'Непременными представителями деревенского сада являются многолетние цветы'
        response = self.client.get(reverse('index'))
        self.assertContains(response, caption)

        PerProduct.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, caption)

        #--

        FruitProduct.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class IndexTestNotExists(TestCase):
    fixtures = ['fixtures/index.json', ]

    def setUp(self):
        self.client = Client()

    def test_index_not_exists(self):
        """ Test index not exists """ 
        Index.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 404)
