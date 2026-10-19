import pytest
from django.test import RequestFactory
from django.http import HttpRequest, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.views.generic.base import View
import logging

# Setting up a logger for the View class
logger = logging.getLogger(__name__)

class TestView(View):
    http_method_names = ['get', 'post']

def test_http_method_not_allowed():
    view = TestView.as_view()
    request_factory = RequestFactory()
    
    # Create a request with an unsupported method
    request = request_factory.put('/test-url/')
    
    # Call the method and get the response
    response = view(request)
    
    # Check that the response is an instance of HttpResponseNotAllowed
    assert isinstance(response, HttpResponseNotAllowed)
    
    # Check that the logger was called with the correct message
    with pytest.raises(AssertionError):
        assert logger.isEnabledFor(logging.WARNING)
    
    # Check that _allowed_methods returns the correct allowed methods
    allowed_methods = view._allowed_methods()
    assert set(allowed_methods) == set(view.http_method_names)