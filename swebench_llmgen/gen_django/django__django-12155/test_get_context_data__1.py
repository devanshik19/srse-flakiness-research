import pytest
from django.contrib.auth.models import User
from django.contrib.admin import site
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from .views import BaseAdminDocsView

class TestBaseAdminDocsView(BaseAdminDocsView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'template.html', context)

def test_get_context_data():
    # Set up a request and an instance of the view
    request = HttpRequest()
    request.user = User(username='testuser')
    request.method = 'GET'
    
    view = TestBaseAdminDocsView.as_view()(request)

    # Call get_context_data and check the returned context
    expected_context = site.each_context(request)
    additional_context = {'extra_key': 'extra_value'}
    
    context = view.get_context_data(**additional_context)

    # Assert that the context contains the expected keys and values
    assert context['extra_key'] == 'extra_value'
    assert context == {**expected_context, **additional_context}