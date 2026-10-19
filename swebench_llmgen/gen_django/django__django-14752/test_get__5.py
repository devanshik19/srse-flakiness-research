import pytest
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse
from django.test import Client

from django.contrib.admin.views.autocomplete import AutocompleteJsonView

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def autocomplete_view():
    return AutocompleteJsonView()

def test_get_success(autocomplete_view, client, user):
    # Simulate user permissions
    client.login(username='testuser', password='testpassword')
    
    # Mock the methods used inside AutocompleteJsonView.get
    autocomplete_view.process_request = lambda req: ('test', None, None, 'id')
    autocomplete_view.get_queryset = lambda: [user]
    autocomplete_view.get_context_data = lambda: {'object_list': [user], 'page_obj': type('obj', (object,), {'has_next': lambda: False})()}

    response = autocomplete_view.get(client.get(reverse('admin:auth_user_autocomplete')), term='test')

    assert isinstance(response, JsonResponse)
    data = response.json()
    assert 'results' in data
    assert len(data['results']) == 1
    assert data['results'][0]['id'] == str(user.id)
    assert data['results'][0]['text'] == str(user)

def test_get_permission_denied(autocomplete_view, client):
    response = autocomplete_view.get(client.get(reverse('admin:auth_user_autocomplete')), term='test')
    assert response.status_code == 403  # Check if it raises PermissionDenied