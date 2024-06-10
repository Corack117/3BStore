import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from applications.users.models import User

@pytest.fixture(scope='class')
def sample_user_administrator():
    user = User.objects.create_user(
        username="corack",
        password="pass123",
        email="orcheko@gmail.com",
        first_name="Sergio",
        last_name="Ordaz",
        is_staff=True
    )
    yield user
    user.delete()

@pytest.fixture(scope='class')
def sample_user():
    user = User.objects.create_user(
        username="mortel",
        password="pass123",
        email="mortel@gmail.com",
        first_name="Marcos",
        last_name="Ordaz"
    )
    yield user
    user.delete()