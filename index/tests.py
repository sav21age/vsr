from django.test import TestCase, Client
from django.urls import reverse

from conifers.models import ConiferProduct
from deciduous.models import DecProduct
from fruits.models import FruitProduct
from index.models import Index
from perennials.models import PerProduct


fixtures = [
    'fixtures/plants.json',
    'fixtures/conifers.json',
    'fixtures/deciduous.json',
    'fixtures/fruits.json',
    'fixtures/perennials.json',
    'fixtures/index.json',
]


class IndexTest(TestCase):
    fixtures = fixtures
    
    def setUp(self):
        self.client = Client()

    def test_index(self):
        """ Test index """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class IndexTestNotExists(TestCase):
    fixtures = fixtures

    def setUp(self):
        self.client = Client()

    def test_index_not_exists(self):
        """ Test index not exists """ 
        Index.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 404)


class IndexCaptionsTest(TestCase):
    fixtures = fixtures
    
    def setUp(self):
        self.client = Client()

    def test_conifers_caption(self):
        """ Test conifers caption """

        caption = 'Хвойные – благородные растения, которые позволяют саду оставаться привлекательным и зеленым круглый год'
        response = self.client.get(reverse('index'))
        self.assertContains(response, caption)

        ConiferProduct.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, caption)

    def test_deciduous_caption(self):
        """ Test deciduous caption """

        caption = 'Лиственные деревья и кустарники – это обычно растения с черешковыми пластинчатыми листьями'
        response = self.client.get(reverse('index'))
        self.assertContains(response, caption)

        DecProduct.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, caption)

    def test_perennials_caption(self):
        """ Test perennials caption """

        caption = 'Непременными представителями деревенского сада являются многолетние цветы'
        response = self.client.get(reverse('index'))
        self.assertContains(response, caption)
        
        PerProduct.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, caption)

    def test_fruits_caption(self):
        """ Test fruits caption """

        FruitProduct.objects.all().delete()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
