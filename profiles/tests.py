from django.urls import reverse
from viride.tests import AnonymousUserTestCase

APP = 'profiles'


class ProfileAnonyUserTest(AnonymousUserTestCase):
    fixtures = ['fixtures/db.json', ]

    def test_detailview(self):
        """ Test DetailView anonymous user """

        response = self.client.get(reverse('{0}:{1}'.format(APP, 'index')))
        self.assertEqual(response.status_code, 302)