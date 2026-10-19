import pytest
from django.contrib.auth.models import User
from django.contrib.admin.sites import site
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.urls import reverse

@pytest.fixture
def user_with_permission():
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def user_without_permission():
    user = User.objects.create_user(username='nopermuser', password='nopermpass')
    return user

@pytest.fixture
def admin_view(client, user_with_permission):
    client.login(username='testuser', password='testpass')
    return client

def test_get_returns_json_response(admin_view):
    url = reverse('admin:app_model_autocomplete')  # replace with actual URL name for autocomplete view
    response = admin_view.get(url, {'term': 'example'})

    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert 'results' in response.json()
    assert 'pagination' in response.json()

def test_get_permission_denied(user_without_permission, client):
    url = reverse('admin:app_model_autocomplete')  # replace with actual URL name for autocomplete view
    client.login(username='nopermuser', password='nopermpass')

    with pytest.raises(PermissionDenied):
        client.get(url, {'term': 'example'})

def test_get_no_results(admin_view):
    url = reverse('admin:app_model_autocomplete')  # replace with actual URL name for autocomplete view
    response = admin_view.get(url, {'term': 'nonexistent'})

    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert response.json() == {'results': [], 'pagination': {'more': False}}