import pytest

from app.factories import EUserFactory
from app.models import EUser

pytestmark = pytest.mark.django_db


def test_factory_instance(e_user_factory):
    assert e_user_factory == EUserFactory


def test_model_instance(e_user):
    assert isinstance(e_user, EUser)


#
#
def test_multiple_users(e_user_factory):
    test1: EUser = e_user_factory(username='Test1')
    test2: EUser = e_user_factory(username='Test2')
    test3: EUser = e_user_factory(username='Test3')

    assert test1.username == 'Test1'
    assert test2.username == 'Test2'
    assert test3.username == 'Test3'

