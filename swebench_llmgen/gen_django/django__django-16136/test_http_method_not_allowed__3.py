import pytest
from django.http import HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.views.generic.base import View

class TestView(View):
    http_method_names = ['get', 'post']

    def _allowed_methods(self):
        return self.http_method_names

@pytest.mark.django_db
def test_http_method_not_allowed(client):
    view_instance = TestView.as_view()
    request = client.post('/fake-url/')  # Simulating a POST request
    response = view_instance(request)

    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert 'get' in response['Allow']
    assert 'post' not in response['Allow']