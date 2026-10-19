import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse

@pytest.fixture
def admin_site():
    return AdminSite()

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='password')
    return user

def test_autocomplete_view(admin_site, user, client):
    client.login(username='testuser', password='password')
    
    # Define a sample request for the autocomplete view
    request = client.get(reverse('admin:your_app_name_modelname_autocomplete'))  # Adjust 'your_app_name_modelname' accordingly
    
    # Invoke the autocomplete view
    response = admin_site.autocomplete_view(request)

    # Check for a successful response
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200