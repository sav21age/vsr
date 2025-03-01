from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from carts.models import Cart, CartItem
from conifers.models import ConiferProductPrice
from orders.models import Order, OrderStatus
from profiles.forms import ProfileUpdateForm
from viride.tests import AnonymUserTestCase, AuthUserTestCase


APP = 'profiles'
URL_LIST = ['index', 'update', 'order_list', 'favorites',]

fixtures = [
    'fixtures/plants.json',
    'fixtures/conifers.json',
    'fixtures/orders.json',
    'fixtures/contenttypes.json',
    'fixtures/auth.json', 
    'fixtures/profiles.json', 
]

class ProfileAnonymUserTest(AnonymUserTestCase):
    fixtures = fixtures

    def test_profile(self):
        """ Test profile anonym user """

        for url in URL_LIST:
            response = self.client.get(reverse(f"{APP}:{url}"))
            self.assertEqual(response.status_code, 302)


class ProfileAuthUserTest(AuthUserTestCase):
    fixtures = fixtures

    def test_profile(self):
        """ Test profile auth user """

        for url in URL_LIST:
            response = self.client.get(reverse(f"{APP}:{url}"))
            self.assertEqual(response.status_code, 200)

    def test_profile_order_detail(self):
        """ Test profile order detail auth user """

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

        order = Order.objects.create(
            user=self.request.user,
            customer_first_name='Денис',
            customer_last_name='Патрушев',
            customer_email='test@test.com',
            customer_phone_number='+7 (777) 777-77-77',
            customer_comment='',
            ip='127.0.0.1',
            user_agent='',
            status=OrderStatus.objects.get(id=1),
        )

        order.number = str(order.id).rjust(8, '0')
        order.save()

        response = self.client.get(
            reverse(f"{APP}:order_detail", kwargs={'pk': order.id}))
        self.assertEqual(response.status_code, 200)

    # def test_profile_user_not_exists(self):
    #     """ Test profile user not exists """

    #     user = User.objects.none()
    #     self.request.user = user

    #     for url in URL_LIST:
    #         response = self.client.get(reverse(f"{APP}:{url}"))
    #         self.assertEqual(response.status_code, 404)


class ProfileFormUserAuthTest(AuthUserTestCase):
    fixtures = fixtures

    def test_form(self):
        """ Test profile form """

        self.form_data = {
            'first_name': 'Денис',
            'last_name': 'Патрушев',
            'phone_number': '+7 (777) 777-77-77',
        }

        form = ProfileUpdateForm(data=self.form_data)
        self.assertTrue(form.is_valid())

        response = self.client.post(
            reverse(f"{APP}:update"), data=self.form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(form['first_name'].value(), 'Денис')
        self.assertEqual(form['last_name'].value(), 'Патрушев')
        self.assertEqual(form['phone_number'].value(), '+7 (777) 777-77-77')

    def test_form_fail(self):
        """ Test profile form """

        self.form_data = {
            'first_name': 'Д',
            'last_name': 'П',
            'phone_number': 'whatever',
        }

        form = ProfileUpdateForm(data=self.form_data)
        self.assertEqual(form.is_valid(), False)

        response = self.client.post(
            reverse(f"{APP}:update"), data=self.form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)