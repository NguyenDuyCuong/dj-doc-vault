from factory import Faker
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "dj_doc_vault_auth.User"

    name = Faker("name")
    email = Faker("email")
    phone_number = Faker("phone_number")
