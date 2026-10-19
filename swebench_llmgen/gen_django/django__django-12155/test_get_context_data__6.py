import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.views.generic import View
from django.contrib.admindocs.views import BaseAdminDocsView

class TestBaseAdminDocsView(BaseAdminDocsView, View):
    def get(self, request, *args, **kwargs):
        return self.get_context_data(**kwargs)

def test_get_context_data():
    # Create a user and log them in
    user = User.objects.create_user(username='testuser', password='password123')
    request = HttpRequest()
    request.user = user
    request.method = 'GET'

    # Initialize the view
    view = TestBaseAdminDocsView.as_view()
    
    # Call the get method to ensure it's working
    context = view(request)

    # Check if the context contains admin site context
    assert 'site' in context
    assert context['site'] == site

    # Ensure the user is being correctly passed in context
    assert request.user.is_authenticated
    assert request.user.username == 'testuser'