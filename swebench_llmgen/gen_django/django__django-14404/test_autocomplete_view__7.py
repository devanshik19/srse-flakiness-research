import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.admin import site
from django.test import RequestFactory
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.http import JsonResponse

class TestAdminSite:
    def setup_method(self):
        self.admin_site = site
        self.request_factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.admin_site.register(User)

    def test_autocomplete_view(self):
        self.client.login(username='testuser', password='password')
        request = self.request_factory.get(reverse('admin:auth_user_autocomplete'))
        response = self.admin_site.autocomplete_view(request)
        
        assert isinstance(response, JsonResponse)
        assert response.status_code == 200
        assert 'results' in response.json()  # Check if 'results' key is in the response

        self.client.logout()

    def test_autocomplete_view_not_authenticated(self):
        request = self.request_factory.get(reverse('admin:auth_user_autocomplete'))
        response = self.admin_site.autocomplete_view(request)

        assert response.status_code == 403  # Expecting forbidden for non-authenticated user