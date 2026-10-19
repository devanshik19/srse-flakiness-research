import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse

@pytest.fixture
def admin_site():
    return AdminSite()

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

def test_autocomplete_view(authenticated_client, admin_site, user):
    authenticated_client.login(username='testuser', password='testpass')
    request = authenticated_client.get(reverse('admin:app_name_model_autocomplete'))  # Use actual auotocomplete URL

    response = admin_site.autocomplete_view(request)

    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    # Check response content if necessary
    # assert response.content == ...

def test_autocomplete_view_unauthenticated(client, admin_site):
    request = client.get(reverse('admin:app_name_model_autocomplete'))  # Use actual autocomplete URL

    response = admin_site.autocomplete_view(request)

    assert response.status_code == 302  # Expecting redirect for unauthenticated user
    assert response.url.startswith('/admin/login/')  # Expecting redirect to login page