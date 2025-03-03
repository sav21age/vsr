import json

from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase
from django.urls import reverse

from carts.models import Cart, CartItem
from carts.views import get_ip
from conifers.models import ConiferProductPrice
from viride.tests import AnonymUserTestCase, AuthUserTestCase

APP = 'carts'

fixtures = [
    'fixtures/plants.json',
    'fixtures/conifers.json',
    'fixtures/contenttypes.json',
    'fixtures/auth.json',
    'fixtures/carts.json', 
]


class GetIpTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_get_ip(self):
        """
        Test the get Client IP fuction with a request.
        """

        request = self.factory.get(reverse(f"{APP}:index"))
        ip = get_ip(request)
        self.assertEqual(ip, '127.0.0.1')
        
        request = self.factory.get(
            reverse(f"{APP}:index"),
            HTTP_X_FORWARDED_FOR='203.0.113.195,2001:db8:85a3:8d3:1319:8a2e:370:7348,198.51.100.178'
        )
        ip = get_ip(request)
        self.assertEqual(ip, '203.0.113.195')

#--


class CartAuthUserTestCase(AuthUserTestCase):
    fixtures = fixtures

    def setUp(self):
        super().setUp()

        self.cart, _ = Cart.objects.get_or_create(
            user=self.request.user,
            defaults={
                'ip': '127.0.0.1',
                'user_agent': 'None',
            },
        )

        self.obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        session = self.client.session
        session['cart_id'] = self.cart.id
        session.save()

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)


class CartAnonymUserTest(AnonymUserTestCase):
    fixtures = fixtures

    def setUp(self):
        super().setUp()

        defaults = {
            'ip': '127.0.0.1',
            'user_agent': 'None',
        }

        self.cart = Cart(**defaults)
        self.cart.save()

        self.obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        session = self.client.session
        session['cart_id'] = self.cart.id
        session.save()

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)

# --


class IndexCartTestMixin():
    def test_show_cart_ok(self):
        """ Test show cart """

        response = self.client.get(reverse(f"{APP}:index"))
        self.assertEqual(response.status_code, 200)


class IndexCartAuthUserTest(IndexCartTestMixin, CartAuthUserTestCase):
    def test_indexview_cart_user_not_exists(self):
        """ Test IndexView for auth user with session """

        Cart.objects.filter(user=self.request.user).delete()

        defaults = {
            'ip': '127.0.0.1',
            'user_agent': 'None',
        }

        cart = Cart(**defaults)
        cart.save()

        session = self.client.session
        session['cart_id'] = cart.id
        session.save()

        response = self.client.get(reverse(f"{APP}:index"))
        self.assertEqual(response.status_code, 200)

    def test_indexview_cart_not_exists(self):
        """ Test IndexView for auth user with session """

        Cart.objects.filter(user=self.request.user).delete()

        response = self.client.get(reverse(f"{APP}:index"))
        self.assertEqual(response.status_code, 200)


class IndexCartAnonymUserTest(IndexCartTestMixin, CartAnonymUserTest):

    def test_indexview_cart_not_exists(self):
        """ Test IndexView for auth user with session """

        Cart.objects.filter(id=self.cart.id).delete()

        response = self.client.get(reverse(f"{APP}:index"))
        self.assertEqual(response.status_code, 200)
# --


class AddCartTestMixin(object):
    def test_get_request_fail(self):
        """ Test get request fail """

        response = self.client.get(reverse(f"{APP}:add"))
        self.assertEqual(response.status_code, 404)

    def test_post_request_fail(self):
        """ Test post request fail """

        response = self.client.post(reverse(f"{APP}:add"))
        self.assertEqual(response.status_code, 404)

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
                         '{"cart": {"total_quantity": 2}}')

        obj = ConiferProductPrice.objects.last()
        ct = ContentType.objects.get_for_model(obj)

        json_data = {
            'id': obj.id,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 3}}')

        response = self.client.get(reverse(f"{APP}:index"))
        self.assertEqual(response.status_code, 200)
    

class AddCartAuthUserTest(AddCartTestMixin, AuthUserTestCase):
    fixtures = fixtures

    def setUp(self):
        super().setUp()

        self.cart, _ = Cart.objects.get_or_create(
            user=self.request.user,
            defaults={
                'ip': '127.0.0.1',
                'user_agent': 'None',
            },
        )

        self.obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        session = self.client.session
        session['cart_id'] = self.cart.id
        session.save()

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)


class AddCartAnonymUserTest(AddCartTestMixin, AnonymUserTestCase):
    fixtures = fixtures

    def setUp(self):
        super().setUp()

        defaults = {
            'ip': '127.0.0.1',
            'user_agent': 'None',
        }

        self.cart = Cart(**defaults)
        self.cart.save()

        self.obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        session = self.client.session
        session['cart_id'] = self.cart.id
        session.save()

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)

    def test_session(self):
        """ Test IndexView for anonymous user """
        obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(obj)

        json_data = {
            'id': obj.id,
            'ct_id': ct.id,
        }

        session = self.client.session
        session.pop('cart_id')
        session.save()

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')
        
    # def test_indexview_cart_not_exists(self):
    #     """ Test IndexView for auth user with session """

    #     defaults = {
    #         'ip': '127.0.0.1',
    #         'user_agent': 'None',
    #     }

    #     Cart.objects.create(
    #         id=self.cart.id,
    #         **defaults,
    #     )

    #     response = self.client.get(reverse(f"{APP}:index"))
    #     self.assertEqual(response.status_code, 200)


class UpdateCartTestMixin():
    def test_get_request_fail(self):
        """ Test get request fail """

        response = self.client.get(reverse(f"{APP}:update"))
        self.assertEqual(response.status_code, 404)

    def test_post_request_fail(self):
        """ Test post request fail """

        response = self.client.post(reverse(f"{APP}:update"))
        self.assertEqual(response.status_code, 404)

    def test_update_add_item(self):
        """  """
        json_data = {
            'id': self.obj.id,
            'ci_id': self.cart_item.id,
            'value': '+',
        }

        response = self.client.post(
            reverse(f"{APP}:update"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content.decode('utf-8'))
        self.assertEqual(res['cart']['total_quantity'], 3)

    def test_update_remove_item(self):
        """  """
        json_data = {
            'id': self.obj.id,
            'ci_id': self.cart_item.id,
            'value': '-',
        }

        response = self.client.post(
            reverse(f"{APP}:update"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content.decode('utf-8'))
        self.assertEqual(res['cart']['total_quantity'], 1)

        response = self.client.post(
            reverse(f"{APP}:update"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content.decode('utf-8'))
        self.assertEqual(res['cart']['total_quantity'], 1)

    def test_request_ci_id_fail(self):
        json_data = {
            'ci_id': 'test',
            'value': '+',
        }

        response = self.client.post(
            reverse(f"{APP}:update"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_request_value_fail(self):
        json_data = {
            'ci_id': self.cart_item.id,
            'value': '?',
        }

        response = self.client.post(
            reverse(f"{APP}:update"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_cart_item_does_not_exists(self):
        json_data = {
            'ci_id': self.cart_item.id,
            'value': '+',
        }

        # Cart.objects.filter(user=self.request.user).delete()
        CartItem.objects.filter(cart=self.cart).delete()

        response = self.client.post(
            reverse(f"{APP}:update"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_cart_delete_500(self):
        json_data = {
            'ci_id': self.cart_item.id,
            'value': '+',
        }

        # Cart.objects.filter(user=self.request.user).delete()
        Cart.objects.filter(id=self.cart.id).delete()

        response = self.client.post(
            reverse(f"{APP}:update"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 500)


class UpdateCartAuthUserTest(UpdateCartTestMixin, AuthUserTestCase):
    fixtures = fixtures

    def setUp(self):
        super().setUp()

        self.cart, _ = Cart.objects.get_or_create(
            user=self.request.user,
            defaults={
                'ip': '127.0.0.1',
                'user_agent': 'None',
            },
        )

        session = self.client.session
        session['cart_id'] = self.cart.id
        session.save()

        self.obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 2}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)


class UpdateCartAnonymUserTest(UpdateCartTestMixin, AnonymUserTestCase):
    fixtures = fixtures

    def setUp(self):
        super().setUp()

        defaults = {
            'ip': '127.0.0.1',
            'user_agent': 'None',
        }

        self.cart = Cart(**defaults)
        self.cart.save()

        self.obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)


        session = self.client.session
        session['cart_id'] = self.cart.id
        session.save()

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 2}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)


# --


class RemoveCartTestMixin():
    def test_get_request_fail(self):
        """ Test get request fail """

        response = self.client.get(reverse(f"{APP}:remove"))
        self.assertEqual(response.status_code, 404)

    def test_post_request_fail(self):
        """ Test post request fail """

        response = self.client.post(reverse(f"{APP}:remove"))
        self.assertEqual(response.status_code, 404)

    def test_remove_item(self):
        """  """
        json_data = {
            'ci_id': self.cart_item.id,
        }

        response = self.client.post(
            reverse(f"{APP}:remove"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content.decode('utf-8'))
        self.assertEqual(res['cart']['total_quantity'], 0)

    def test_request_ci_id_fail(self):
        json_data = {
            'ci_id': 'test',
        }

        response = self.client.post(
            reverse(f"{APP}:remove"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_cart_item_does_not_exists(self):
        json_data = {
            'ci_id': self.cart_item.id,
        }

        # Cart.objects.filter(user=self.request.user).delete()
        CartItem.objects.filter(cart=self.cart).delete()

        response = self.client.post(
            reverse(f"{APP}:remove"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_cart_delete_500(self):
        json_data = {
            'ci_id': self.cart_item.id,
        }

        # Cart.objects.filter(user=self.request.user).delete()
        Cart.objects.filter(id=self.cart.id).delete()

        response = self.client.post(
            reverse(f"{APP}:remove"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 500)


class RemoveCartAuthUserTest(RemoveCartTestMixin, AuthUserTestCase):
    fixtures = fixtures

    def setUp(self):
        super().setUp()

        self.cart, _ = Cart.objects.get_or_create(
            user=self.request.user,
            defaults={
                'ip': '127.0.0.1',
                'user_agent': 'None',
            },
        )

        self.obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        session = self.client.session
        session['cart_id'] = self.cart.id
        session.save()

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)


class RemoveCartAnonymUserTest(RemoveCartTestMixin, AnonymUserTestCase):
    fixtures = fixtures

    def setUp(self):
        super().setUp()

        defaults = {
            'ip': '127.0.0.1',
            'user_agent': 'None',
        }

        self.cart = Cart(**defaults)
        self.cart.save()

        self.obj = ConiferProductPrice.objects.first()
        ct = ContentType.objects.get_for_model(self.obj)

        json_data = {
            'id': self.obj.id,
            'ct_id': ct.id,
        }

        session = self.client.session
        session['cart_id'] = self.cart.id
        session.save()

        response = self.client.post(
            reverse(f"{APP}:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)

