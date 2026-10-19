import pytest
from django.http import HttpRequest
from django.views.generic.base import View
from django.contrib.auth.models import User

class TestView(View):
    http_method_names = ['get']

    def _allowed_methods(self):
        return self.http_method_names

def test_http_method_not_allowed(client):
    view = TestView.as_view()
    request = HttpRequest()
    request.method = 'POST'  # Using a method not allowed
    request.path = '/test/'

    response = view(request)

    assert response.status_code == 405
    assert response['Allow'] == 'GET'  # Ensuring the allowed method is returned in the response