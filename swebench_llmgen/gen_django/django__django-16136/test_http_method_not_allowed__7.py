import pytest
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.base import View
import logging

logger = logging.getLogger(__name__)

class TestView(View):
    http_method_names = ['get', 'post']

def test_http_method_not_allowed_get(client):
    view = TestView.as_view()
    request = client.post(reverse('some-view-name'))  # Assuming 'some-view-name' is a valid URL pattern
    response = view(request)

    # Assert that the response is of type HttpResponseNotAllowed
    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert logger.warning.call_count == 1

def test_http_method_not_allowed_post(client):
    view = TestView.as_view()
    request = client.get(reverse('some-view-name'))  # Assuming 'some-view-name' is a valid URL pattern
    response = view(request)

    # Assert that the response is of type HttpResponseNotAllowed
    assert isinstance(response, HttpResponseNotAllowed)
    assert response.status_code == 405
    assert logger.warning.call_count == 1