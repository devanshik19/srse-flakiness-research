import pytest
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.views import View
from .views import BaseAdminDocsView

class MockAdminSite(AdminSite):
    def each_context(self, request):
        return {'user': request.user}

admin.site = MockAdminSite(name='test_admin')

class TestBaseAdminDocsView(BaseAdminDocsView):
    def dispatch(self, request):
        return HttpRequest()

# Test case for the get_context_data method
def test_get_context_data():
    view = TestBaseAdminDocsView()
    
    # Simulate a request with a user
    user = User(username='testuser')
    HttpRequest.user = user  # Set the user on the request
    request = HttpRequest()
    request.user = user
    
    # Call the method
    context = view.get_context_data(request=request, additional='data')
    
    assert 'additional' in context
    assert context['additional'] == 'data'
    assert context['user'] == user