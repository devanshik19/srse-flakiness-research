import pytest
from django.http import HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import RequestFactory
from django.views.generic import View

class TestView(View):
    http_method_names = ['get', 'post']

def test_http_method_not_allowed_get():
    request_factory = RequestFactory()
    view = TestView.as_view()
    request = request_factory.get('/')
    
    # This view only allows GET and POST methods, we will send PUT to test the method not allowed.
    response = view(request)

    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert 'GET' not in response['Allow']
    assert 'POST' not in response['Allow']

def test_http_method_not_allowed_post():
    request_factory = RequestFactory()
    view = TestView.as_view()
    request = request_factory.post('/')
    
    # This view only allows GET and POST methods, we will send DELETE to test the method not allowed.
    request.method = 'DELETE'
    response = view(request)

    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert 'GET' not in response['Allow']
    assert 'POST' not in response['Allow']