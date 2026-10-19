import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import RequestFactory
from django.contrib import admin
from .views import BaseAdminDocsView

class TestBaseAdminDocsView:
    @pytest.fixture
    def view(self):
        return BaseAdminDocsView()

    @pytest.fixture
    def request(self):
        return HttpRequest()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='testpass')

    def test_get_context_data(self, view, request, user):
        request.user = user
        view.request = request
        # Add some additional context to test merging
        additional_context = {'some_key': 'some_value'}
        context = view.get_context_data(**additional_context)
        
        # Assert that context contains the merged values
        assert context['some_key'] == 'some_value'
        assert 'user' in context
        assert context['user'] == user
        assert 'admin' in context

        # Test that each_context is properly called and merged into the context
        assert 'site' in context['admin']