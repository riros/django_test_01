import factory
from faker import Factory as FakerFactory

from app.models import (
    EUser, CashTransaciton
)

faker = FakerFactory.create()
faker.seed(983843)


class EUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EUser

    username = factory.LazyAttribute(lambda x: faker.name())
    middle_name = factory.LazyAttribute(lambda x: faker.name())
    email = factory.LazyAttribute(lambda x: faker.email())
    tin = factory.LazyAttribute(lambda x: faker.pyint())
