import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse

@pytest.fixture
def admin_site():
    return AdminSite(name='test_admin')

@pytest.fixture
def user(client):
    user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
    client.login(username='admin', password='admin')
    return user

def test_autocomplete_view(admin_site, user):
    url = reverse('admin:app_name_modelname_autocomplete')  # Replace app_name_modelname with actual app/model
    response = admin_site.autocomplete_view(user)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200