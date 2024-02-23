from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory


class AuthUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # self.user = User.objects.create(username='testuser', password='12345', is_active=True, is_staff=True, is_superuser=True)
        self.user = User.objects.create(username='test', email='test@test.com')
        self.user.set_password('123456789')
        self.user.save()
        self.user = authenticate(username='test', password='123456789')
        login = self.client.login(username='test', password='123456789')
        self.assertTrue(login)

        self.factory = RequestFactory()
        self.request = self.factory.get('')
        self.request.user = self.user


class AnonymousUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
