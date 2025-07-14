from django.urls import reverse
import pytest

from src.users.models import User


@pytest.mark.django_db()
def test_login(api_client, user: User):
    data = {
        "email": user.email,
        "password": 'Teste@123'
    }
    response = api_client.post(
        reverse('login'), data=data, format='json')
    assert response.status_code == 200
