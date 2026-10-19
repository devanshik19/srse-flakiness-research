import pytest
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from django.utils.module_loading import import_string
from django.contrib.auth.models import User
from django.core.handlers.base import BaseHandler

# Sample middleware for testing
class TestMiddleware:
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

# Add the test middleware to settings for testing
settings.MIDDLEWARE = ['path.to.TestMiddleware']

@pytest.fixture
def base_handler():
    return BaseHandler()

def test_load_middleware_sync(base_handler):
    base_handler.load_middleware(is_async=False)
    assert len(base_handler._view_middleware) == 1
    assert len(base_handler._template_response_middleware) == 1
    assert len(base_handler._exception_middleware) == 1
    assert base_handler._middleware_chain is not None

def test_load_middleware_async(base_handler):
    settings.MIDDLEWARE = ['path.to.TestMiddleware']
    base_handler.load_middleware(is_async=True)
    assert len(base_handler._view_middleware) == 1
    assert len(base_handler._template_response_middleware) == 1
    assert len(base_handler._exception_middleware) == 1
    assert base_handler._middleware_chain is not None

def test_middleware_not_used(base_handler):
    settings.MIDDLEWARE = ['path.to.TestMiddleware', 'django.core.exceptions.MiddlewareNotUsed']
    with pytest.raises(MiddlewareNotUsed):
        base_handler.load_middleware(is_async=False)

def test_middleware_improperly_configured(base_handler):
    settings.MIDDLEWARE = ['path.to.InvalidMiddleware']
    with pytest.raises(ImproperlyConfigured):
        base_handler.load_middleware(is_async=False)