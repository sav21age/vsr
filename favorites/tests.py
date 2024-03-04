import json
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from carts.models import Cart, CartItem
from conifers.models import ConiferProduct, ConiferProductPrice
from favorites.models import Favorites
from viride.tests import AnonymUserTestCase, AuthUserTestCase


APP = 'favorites'


class FavoritesAuthUserTest(AuthUserTestCase):
    fixtures = ['fixtures/db.json', ]

    def test_set(self):
        self.obj = ConiferProduct.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        response = self.client.get(
            reverse(f"{APP}"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '{"state": true}')

        response = self.client.get(
            reverse(f"{APP}"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '{"state": false}')

    def test_set_fail(self):
        """ Test add to cart for anonymous user fail """

        json_data = {
            'id': 'test',
            'ct_id': 10000,
        }

        response = self.client.get(
            reverse(f"{APP}"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

        json_data = {
            'id': 10000,
            'ct_id': 'test',
        }

        response = self.client.get(
            reverse(f"{APP}"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

        obj = ConiferProduct.objects.first()
        ct = ContentType.objects.get_for_model(obj)

        json_data = {
            'id': 10000,
            'ct_id': ct.id,
        }

        response = self.client.get(
            reverse(f"{APP}"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

        ct = ContentType.objects.get_for_model(Favorites)

        json_data = {
            'id': 10000,
            'ct_id': ct.id,
        }

        response = self.client.get(
            reverse(f"{APP}"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_get_request_fail(self):
        """ Test get request fail """

        response = self.client.get(reverse(f"{APP}"))
        self.assertEqual(response.status_code, 405)

    def test_post_request_fail(self):
        """ Test post request fail """

        response = self.client.post(reverse(f"{APP}"))
        self.assertEqual(response.status_code, 405)


class FavoritesAnonymUserTest(AnonymUserTestCase):
    fixtures = ['fixtures/db.json', ]

    def test_set(self):
        self.obj = ConiferProduct.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        response = self.client.get(
            reverse(f"{APP}"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)
