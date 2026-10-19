import pytest
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from django.urls import get_resolver
from django.utils.module_loading import import_string
from django.contrib.auth.models import User
from django.core.handlers.base import BaseHandler

# A dummy middleware for testing
class DummyMiddleware:
    sync_capable = True
    async_capable = False

    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return None

# A dummy middleware that raises MiddlewareNotUsed
class DummyMiddlewareNotUsed:
    sync_capable = True
    async_capable = False

    def __init__(self, get_response):
        raise MiddlewareNotUsed("DummyMiddlewareNotUsed example")

@pytest.fixture
def settings_with_middlewares():
    # Temporarily modify settings for testing
    original_middleware = settings.MIDDLEWARE
    settings.MIDDLEWARE = [
        'path.to.DummyMiddleware',  # Replace with full path to DummyMiddleware
        'path.to.DummyMiddlewareNotUsed',  # Adjust path as necessary
    ]
    yield
    settings.MIDDLEWARE = original_middleware

def test_load_middleware(settings_with_middlewares):
    handler = BaseHandler()

    # Test loading middleware synchronously
    handler.load_middleware(is_async=False)
    
    assert isinstance(handler._view_middleware[0], types.FunctionType)
    assert isinstance(handler._template_response_middleware[0], types.FunctionType)
    assert isinstance(handler._exception_middleware[0], types.FunctionType)
    assert callable(handler._middleware_chain)

    # Test loading middleware asynchronously
    handler.load_middleware(is_async=True)
    
    assert isinstance(handler._view_middleware[0], types.FunctionType)
    assert isinstance(handler._template_response_middleware[0], types.FunctionType)
    assert isinstance(handler._exception_middleware[0], types.FunctionType)
    assert callable(handler._middleware_chain)

    # Test behavior when middleware raises MiddlewareNotUsed
    with pytest.raises(ImproperlyConfigured):
        handler.load_middleware(is_async=False)