import pytest
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic.list import BaseListView
from django.apps import apps
from django.contrib.admin import AdminSite
from django.contrib.admin.views.autocomplete import AutocompleteJsonView

@pytest.fixture
def user_with_perm(db):
    user = User.objects.create_user(username='testuser', password='password')
    user.user_permissions.add(apps.get_model('auth', 'Permission').objects.get(codename='view_user'))
    return user

@pytest.fixture
def user_without_perm(db):
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def view():
    return AutocompleteJsonView()

def test_get_with_perm(view, client, user_with_perm):
    client.login(username='testuser', password='password')
    url = reverse('admin:your_model_autocomplete')  # Replace 'your_model_autocomplete' with the actual URL name

    response = client.get(url, {'term': 'test'})
    
    assert response.status_code == 200
    assert isinstance(response, JsonResponse)
    assert 'results' in response.json()
    assert 'pagination' in response.json()

def test_get_without_perm(view, client, user_without_perm):
    client.login(username='testuser', password='password')
    url = reverse('admin:your_model_autocomplete')  # Replace 'your_model_autocomplete' with the actual URL name

    with pytest.raises(PermissionDenied):
        client.get(url, {'term': 'test'})

def test_get_no_results(view, client, user_with_perm):
    client.login(username='testuser', password='password')
    url = reverse('admin:your_model_autocomplete')  # Replace 'your_model_autocomplete' with the actual URL name

    response = client.get(url, {'term': 'nonexistent'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['results'] == []
    assert data['pagination']['more'] is False