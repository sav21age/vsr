from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

# from axes.decorators import axes_dispatch


class AuthUserTestCase(TestCase):
    # @axes_dispatch
    def setUp(self):
        self.client = Client()
        # self.user = User.objects.create(username='testuser', password='12345', is_active=True, is_staff=True, is_superuser=True)
        self.user = User.objects.create(username='test', email='test@test.com')
        # self.user.profile = Profile.objects.create(user=self.user)
        self.user.set_password('123456789')
        self.user.save()
        request = HttpRequest()
        self.user = authenticate(request,
                                 username='test@test.com', password='123456789')
        self.client.force_login(self.user)
        # login = self.client.login(username='test', password='123456789')
        # self.assertTrue(login)

        self.factory = RequestFactory()
        self.request = self.factory.get('')
        self.request.user = self.user


class AnonymUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.request = self.factory.get('')


class SitemapTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sitemap(self):
        """ Test sitemap """
        response = self.client.get(
            reverse('django.contrib.sitemaps.views.sitemap'))
        self.assertEqual(response.status_code, 200)
        