from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from conifers.models import ConiferProductPrice
from viride.tests import AnonymousUserTestCase, AuthUserTestCase


APP = 'carts'


class AnonymousUserTest(AnonymousUserTestCase):
    fixtures = ['fixtures/db.json', ]

    def test_indexview_ok(self):
        """ Test IndexView for anonymous user """

        response = self.client.get(reverse(f"{APP}:index"))
        self.assertEqual(response.status_code, 200)

    def test_cart_add_fail(self):
        """ Test add to cart for anonymous user fail """

        response = self.client.get(reverse(f"{APP}:add"))
        self.assertEqual(response.status_code, 404)

        json_data = {
            'id': 'test',
            'ct_id': 10000,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

        json_data = {
            'id': 10000,
            'ct_id': 'test',
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        
        obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(obj)

        json_data = {
            'id': 10000,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        

    def test_cart_add_ok(self):
        """ Test IndexView for anonymous user """
        obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(obj)
        
        json_data = {
            'id': obj.id,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(obj)
        
        json_data = {
            'id': obj.id,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 2}}')

        response = self.client.get(reverse(f"{APP}:index"))
        self.assertEqual(response.status_code, 200)


class AuthUserTest(AuthUserTestCase):
    fixtures = ['fixtures/db.json', ]

    def test_indexview(self):
        """ Test IndexView for auth user """

        response = self.client.get(reverse(f"{APP}:index"))
        self.assertEqual(response.status_code, 200)

    def test_cart_add_fail(self):
        """ Test add to cart for anonymous user fail """

        response = self.client.get(reverse(f"{APP}:add"))
        self.assertEqual(response.status_code, 404)

        json_data = {
            'id': 'test',
            'ct_id': 10000,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

        json_data = {
            'id': 10000,
            'ct_id': 'test',
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

        obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(obj)

        json_data = {
            'id': 10000,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_cart_add_ok(self):
        """ Test cart for auth user """
        obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(obj)

        json_data = {
            'id': obj.id,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(obj)

        json_data = {
            'id': obj.id,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 2}}')

        response = self.client.get(reverse(f"{APP}:index"))
        self.assertEqual(response.status_code, 200)
