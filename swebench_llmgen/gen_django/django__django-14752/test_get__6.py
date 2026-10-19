import pytest
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse

class TestAutocompleteJsonView:

    @pytest.fixture
    def create_user(self):
        return User.objects.create_user(username='testuser', password='testpass')

    def test_get_success(self, client, create_user):
        # Log in the user
        client.login(username='testuser', password='testpass')

        # Set up the expected URL and parameters
        url = reverse('autocomplete-url')  # Replace with the actual URL name
        response = client.get(url, {'term': 'test'})

        assert response.status_code == 200
        assert isinstance(response, JsonResponse)
        assert 'results' in response.json()
        assert 'pagination' in response.json()

    def test_get_permission_denied(self, client):
        url = reverse('autocomplete-url')  # Replace with the actual URL name
        response = client.get(url, {'term': 'test'})

        assert response.status_code == 403  # Forbidden due to permission denied

    def test_get_empty_results(self, client, create_user):
        # Log in the user
        client.login(username='testuser', password='testpass')

        # Set up the expected URL and parameters
        url = reverse('autocomplete-url')  # Replace with the actual URL name
        response = client.get(url, {'term': 'non-existent-term'})

        assert response.status_code == 200
        assert response.json() == {'results': [], 'pagination': {'more': False}}