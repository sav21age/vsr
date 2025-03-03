from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
# from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django_recaptcha.client import RecaptchaResponse

from carts.models import Cart, CartItem
from common.tests import AnonymUserTestCase, AuthUserTestCase
from conifers.models import ConiferProduct, ConiferProductPrice
from orders.models import AcceptingOrders
from orders.views import CreateOrderAnonymUserView, CreateOrderAuthUserView


APP = 'orders'


fixtures = [
    'fixtures/plants.json',
    'fixtures/conifers.json',
    'fixtures/contenttypes.json',
    'fixtures/auth.json',
    'fixtures/orders.json',
]


class InitialCreateOrderAuthUser(AuthUserTestCase):
    def setUp(self):
        super().setUp()

        obj = AcceptingOrders.objects.get()
        obj.name = 'ORDER'
        obj.save()

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
            reverse("carts:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)


class CreateOrderAuthUserFormTest(InitialCreateOrderAuthUser):
    fixtures = fixtures

    def test_form(self):
        """ Test order form """

        form_data = {
            'customer_first_name': 'Денис',
            'customer_last_name': 'Патрушев',
            'customer_email': 'test@test.com',
            'customer_phone_number': '+7 (777) 777-77-77',
            'customer_comment': 'Тест',
        }

        request = self.factory.post(
            reverse(f"{APP}:create"), data=form_data)
        request.user = self.user
        response = CreateOrderAuthUserView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('orders:success'))


class CreateOrderAuthUserFormInvalidTest(InitialCreateOrderAuthUser):
    fixtures = fixtures

    def test_form_invalid(self):
        """ Test order form """

        form_data = {
            'customer_email': 'test@test.com',
            'customer_comment': 'Тест',
        }

        request = self.factory.post(
            reverse(f"{APP}:create"), data=form_data)
        request.user = self.user
        response = CreateOrderAuthUserView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class CreateOrderAuthUserFormPreFilledTest(InitialCreateOrderAuthUser):
    fixtures = fixtures

    def test_form(self):
        """ Test order form """

        form_data = {
            'customer_phone_number': '+7 (777) 777-77-77',
            'customer_comment': 'Тест',
        }

        request = self.factory.post(
            reverse(f"{APP}:create"), data=form_data)

        user = User.objects.get(pk=self.request.user.pk)

        user.first_name = 'Денис'
        user.last_name = 'Патрушев'
        user.save()

        request.user = user
        response = CreateOrderAuthUserView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('orders:success'))


class CreateOrderAuthUserTest(InitialCreateOrderAuthUser):
    fixtures = fixtures

    def test_create_order_ok(self):
        """ Test create order """

        response = self.client.get(reverse(f"{APP}:create"))
        self.assertEqual(response.status_code, 200)


class CreateOrderAuthUserNoCartTest(InitialCreateOrderAuthUser):
    fixtures = fixtures

    def test_no_cart(self):
        Cart.objects.get(user=self.request.user).delete()

        response = self.client.get(reverse(f"{APP}:create"))
        self.assertEqual(response.status_code, 302)


class CreateOrderAuthUserNoCartItemsTest(InitialCreateOrderAuthUser):
    fixtures = fixtures

    def test_no_cart_items(self):
        cart = Cart.objects.get(user=self.request.user)
        CartItem.objects.get(cart=cart).delete()

        response = self.client.get(reverse(f"{APP}:create"))
        self.assertEqual(response.status_code, 302)


class CreateOrderAuthUserCloseUntilAprilTest(AuthUserTestCase):
    fixtures = fixtures

    def test_close_until_april(self):
        obj = AcceptingOrders.objects.get()
        obj.name = 'CLOSE_UNTIL_APRIL'
        obj.save()

        response = self.client.get(reverse(f"{APP}:create"))
        self.assertEqual(response.status_code, 404)


# --


class InitialCreateOrderAnonymUser(AnonymUserTestCase):
    def setUp(self):
        super().setUp()

        obj = AcceptingOrders.objects.get()
        obj.name = 'ORDER'
        obj.save()

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
            reverse("carts:add"), json_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),
                         '{"cart": {"total_quantity": 1}}')

        self.cart_item = CartItem.objects.get(cart=self.cart)


class CreateOrderAnonymUserFormTest(InitialCreateOrderAnonymUser):
    fixtures = fixtures

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_form_invalid(self, mocked_submit):
        """ Test order form """
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)

        form_data = {
            'customer_first_name': 'Денис',
            'customer_last_name': 'Патрушев',
            'customer_email': 'test@test.com',
            'customer_phone_number': '+7 (777) 777-77-77',
            'customer_comment': 'Тест',
            'captcha': 'PASSED',
        }

        request = self.factory.post(
            reverse(f"{APP}:create"), data=form_data)
        request.session = {'cart_id': self.cart.id}

        # middleware = SessionMiddleware(lambda x: x)
        # middleware.process_request(request)
        # request.session.save()
        response = CreateOrderAnonymUserView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.url, reverse('orders:confirm'))
        self.assertEqual(response.url, reverse('orders:success'))

        # order = Order.objects.filter(customer_email='test@test.com').last()

        # session = self.client.session
        # session['order_id'] = order.id
        # session.save()

        # response = self.client.get(
        #     reverse(f"{APP}:confirm"))
        # self.assertEqual(response.status_code, 200)

        # # --

        # form_data = {
        #     'confirm_code': order.confirm_code,
        # }
        # request = self.factory.post(
        #     reverse(f"{APP}:confirm"), data=form_data)

        # request.session = {
        #     'cart_id': self.cart.id,
        #     'order_id': order.id,
        #     'confirm_code_sent': False,
        # }

        # response = ConfirmOrderAnonymView.as_view()(request)
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.url, reverse('orders:success'))


class CreateOrderAnonymUserFormInvalidTest(InitialCreateOrderAnonymUser):
    fixtures = fixtures

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_form_invalid(self, mocked_submit):
        """ Test order form """
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)

        form_data = {
            'customer_email': 'test@test.com',
            'customer_comment': 'Тест',
            'captcha': 'PASSED',
        }

        request = self.factory.post(
            reverse(f"{APP}:create"), data=form_data)
        request.session = {'cart_id': self.cart.id}

        response = CreateOrderAnonymUserView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class CreateOrderAnonymUserTest(InitialCreateOrderAnonymUser):
    fixtures = fixtures

    def test_create_order_ok(self):
        """ Test create order """

        response = self.client.get(reverse(f"{APP}:create"))
        self.assertEqual(response.status_code, 200)


class CreateOrderAnonymUserNoCartTest(InitialCreateOrderAnonymUser):
    fixtures = fixtures

    def test_no_cart(self):
        Cart.objects.get(id=self.cart.id).delete()

        response = self.client.get(reverse(f"{APP}:create"))
        self.assertEqual(response.status_code, 302)


class CreateOrderAnonymUserNoCartItemsTest(InitialCreateOrderAnonymUser):
    fixtures = fixtures

    def test_no_cart_items(self):
        cart = Cart.objects.get(id=self.cart.id)
        CartItem.objects.get(cart=cart).delete()

        response = self.client.get(reverse(f"{APP}:create"))
        self.assertEqual(response.status_code, 302)


class CreateOrderAnonymUserCloseUntilAprilTest(AnonymUserTestCase):
    fixtures = fixtures

    def test_close_until_april(self):
        obj = AcceptingOrders.objects.get()
        obj.name = 'CLOSE_UNTIL_APRIL'
        obj.save()

        response = self.client.get(reverse(f"{APP}:create"))
        self.assertEqual(response.status_code, 404)


# --


class AcceptingOrdersTest(TestCase):
    fixtures = fixtures

    def setUp(self):
        self.client = Client()

    def test_change_accepting_orders(self):
        """ Test change accepting orders """
        with override_settings(CACHE_TIMEOUT=900):
            obj = AcceptingOrders.objects.get()
            obj.name = 'ORDER'
            obj.save()

            con = ConiferProduct.is_visible_objects \
                .prefetch_related('images') \
                .all()[:1].get()

            response = self.client.get(
                reverse("conifers:detail", kwargs={'slug': con.slug}))
            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response, '<p class="mb-1 text-secondary delivery">Самовывоз</p>', html=True)

            obj.name = 'PRE_ORDER'
            obj.save()
            response = self.client.get(
                reverse("conifers:detail", kwargs={'slug': con.slug}))
            self.assertContains(
                response, 'Питомник откроется в начале мая', html=True)

            obj.name = 'CLOSE_UNTIL_APRIL'
            obj.save()
            response = self.client.get(
                reverse("conifers:detail", kwargs={'slug': con.slug}))
            self.assertContains(
                response, 'Питомник закрыт до мая', html=True)
