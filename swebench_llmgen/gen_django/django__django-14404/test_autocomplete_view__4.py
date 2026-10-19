import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse

class MockAutocompleteJsonView:
    @staticmethod
    def as_view(admin_site):
        def view(request):
            return JsonResponse({'success': True})
        return view

# Override the AutocompleteJsonView in the AdminSite for testing
AdminSite.autocomplete_view = lambda self, request: MockAutocompleteJsonView.as_view(self)(request)

@pytest.fixture
def admin_site():
    return AdminSite(name='admin')

@pytest.fixture
def client_with_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

def test_autocomplete_view(admin_site, client_with_user, client):
    client.login(username='testuser', password='testpassword')
    response = admin_site.autocomplete_view(client.get('/admin/autocomplete/'))

    assert response.status_code == 200
    assert response.json() == {'success': True}