import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from app.factories import (
    EUserFactory
)

register(EUserFactory)


@pytest.fixture
def single_entry(e_user, entry_factory):
    entry = entry_factory(euesr=e_user, )
    return entry


@pytest.fixture
def multiple_entries(euser_factory, entry_factory):
    entries = [
        entry_factory(euser=euser_factory(), ),
        entry_factory(euser=euser_factory(), ),
    ]
    # comment_factory(entry=entries[0])
    # comment_factory(entry=entries[1])
    return entries

@pytest.fixture
def client():
    return APIClient()
