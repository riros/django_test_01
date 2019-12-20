from django.test import TestCase
from django.contrib.auth import get_user_model
from base.models import BaseModel


class BaseTestCase(TestCase):
    """
    Test base class to setup a couple users.
    """

    def setUp(self):
        """
        Create those users
        """
        super(BaseTestCase, self).setUp()

    @staticmethod
    def create_user(username, email, password="pw",
                    first_name='', last_name=''):
        """
        Helper method to create a user
        """
        User = get_user_model()
        user = User.objects.create_user(
            username, email, password=password
        )
        if first_name or last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        return user

    def test_create_users(self):
        """
        Create a couple users
        """
        self.john = self.create_user(
            'trane', 'john@example.com',
            first_name='John', last_name="Coltrane")
        self.miles = self.create_user(
            'miles', 'miles@example.com',
            first_name="Miles", last_name="Davis")
        self.assertEqual(True, issubclass(self.miles.__class__, BaseModel))
        self.assertEqual(True, issubclass(self.john.__class__, BaseModel))
