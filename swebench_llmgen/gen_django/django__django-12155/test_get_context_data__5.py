import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.views.generic import TemplateView
from django.urls import reverse
from .views import BaseAdminDocsView

class TestBaseAdminDocsView(BaseAdminDocsView):
    template_name = 'admin/docs/index.html'

@pytest.fixture
def user(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def request_factory():
    return RequestFactory()

def test_get_context_data(user, request_factory):
    view = TestBaseAdminDocsView.as_view()  # Create a callable view
    request = request_factory.get(reverse('admin:index'))
    request.user = user
    response = view(request)

    # Ensure the response context includes the admin context
    assert 'admin' in response.context_data
    assert 'request' in response.context_data
    assert response.status_code == 200

    # Check if additional kwargs passed through get_context_data are included
    additional_kwargs = {'extra_key': 'extra_value'}
    context_data = view(request, **additional_kwargs).context_data
    assert context_data['extra_key'] == 'extra_value'