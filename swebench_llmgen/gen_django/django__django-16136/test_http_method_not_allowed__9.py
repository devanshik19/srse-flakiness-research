import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.test import RequestFactory
from django.views.generic import View

class TestView(View):
    http_method_names = ['get', 'post']

def test_http_method_not_allowed_get():
    view = TestView.as_view()
    request_factory = RequestFactory()
    request = request_factory.post(reverse('some_view_name'))  # Assuming a post request is made
    response = view(request)

    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert 'POST' in response['Allow']  # Assuming 'POST' is an allowed method
    assert 'GET' not in response['Allow']  # Assuming 'GET' is not an allowed method

def test_http_method_not_allowed_post():
    view = TestView.as_view()
    request_factory = RequestFactory()
    request = request_factory.get(reverse('some_view_name'))  # Assuming a get request is made
    response = view(request)

    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert 'GET' in response['Allow']  # Assuming 'GET' is an allowed method
    assert 'POST' not in response['Allow']  # Assuming 'POST' is not an allowed method

def test_http_method_not_allowed_logging(caplog):
    view = TestView.as_view()
    request_factory = RequestFactory()
    request = request_factory.put(reverse('some_view_name'))  # Simulating an unsupported method
    response = view(request)

    assert response.status_code == 405
    assert 'Method Not Allowed' in caplog.text
    assert 'PUT' in caplog.text  # Check the logged method