import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse

class TestAdminSite:
    @pytest.fixture
    def admin_site(self):
        return AdminSite()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='testpass')

    def test_autocomplete_view(self, admin_site, user, rf):
        request = rf.get(reverse('admin:autocomplete_view'))  # Replace with actual URL name if known
        request.user = user
        response = admin_site.autocomplete_view(request)

        assert isinstance(response, JsonResponse)  # Check that the response is a JsonResponse
        assert response.status_code == 200  # Check that the status code is 200