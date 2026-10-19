import pytest
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.admindocs.views import BaseAdminDocsView

class TestBaseAdminDocsView(BaseAdminDocsView, TemplateView):
    template_name = 'admindocs/doc.html'  # Assuming there's a template to use

def test_get_context_data():
    # Create a request object
    request = HttpRequest()
    request.user = User(username='testuser', is_staff=True, is_active=True)
    request.user.set_password('password')
    request.user.save()
    
    # Create an instance of the BaseAdminDocsView subclass
    view = TestBaseAdminDocsView.as_view()
    
    # Call the view to get the response
    response = view(request)
    
    # Get the context data
    context_data = view.get_context_data()
    
    # Assertions
    assert 'request' in context_data
    assert context_data['request'] == request
    assert 'user' in context_data
    assert context_data['user'] == request.user
    assert 'admin' in context_data
    assert context_data['admin'] == site  # Ensuring site context is passed