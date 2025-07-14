from django.db import connections
from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from django.conf import settings
from django.db import connections

from src.users.models import User


# @pytest.fixture(scope='session')
# def django_db_setup():
#     del connections.__dict__["settings"]
#     settings.DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
#     connections._settings = connections.configure_settings( # type: ignore
#         settings.DATABASES)  
#     connections["default"] = connections.create_connection( # type: ignore
#         "default")  


@pytest.fixture(scope="function")
def api_client():
    """
    Fixture to provide an API client
    :return: APIClient
    """
    yield APIClient()

@pytest.fixture
def dummy_user():
    user = User.objects.create(
        name='dummy',
        email='teste@gmail.com',
        age=99
    )
    user.set_password('Teste@123')
    user.save()
    return user

@pytest.fixture
def authenticate_user(api_client, user):
    data = {
        "email": user.email,
        "password": 'Teste@123', 
    }
    
    response = api_client.post(reverse('login'), data=data, format='json')
    token = response.data.get('access_token')  
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client