import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.contrib.admin import site
from django.views.generic import TemplateView
from django.urls import reverse
from yourapp.views import BaseAdminDocsView  # replace 'yourapp' with the actual app name

class TestBaseAdminDocsView(BaseAdminDocsView):
    template_name = 'your_template.html'  # replace with an actual template if needed

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.mark.django_db
def test_get_context_data(request_factory, user):
    request = request_factory.get(reverse('admin:index'))
    request.user = user
    view = TestBaseAdminDocsView.as_view()
    
    # Call the method under test
    context = view(request)

    # Ensure the context includes the admin site context
    assert 'site' in context.context_data
    assert context.context_data['site'] == site
    assert context.context_data['user'] == user