import pytest
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.views.generic.base import View

class TestView(View):
    http_method_names = ['get', 'post']

    def _allowed_methods(self):
        return self.http_method_names

    def dispatch(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

@pytest.mark.django_db
def test_http_method_not_allowed_client(client):
    view = TestView.as_view()
    request = client.post(reverse('dummy-url'))  # Assuming 'dummy-url' is a valid URL
    response = view(request)

    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert 'GET' in response.headers['Allow']  # Assuming GET is allowed
    assert 'POST' in response.headers['Allow']  # Assuming POST is allowed