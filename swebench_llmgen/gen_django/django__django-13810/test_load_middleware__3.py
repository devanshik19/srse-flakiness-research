import pytest
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from django.utils.module_loading import import_string
from django.contrib.auth.models import User
from django.core.handlers.base import BaseHandler

# Sample middleware for testing purposes
class TestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return None

@pytest.fixture
def base_handler():
    return BaseHandler()

@pytest.mark.parametrize("is_async", [True, False])
def test_load_middleware_with_valid_middleware(base_handler, is_async, settings):
    settings.MIDDLEWARE = [
        'path.to.TestMiddleware',
    ]
    
    base_handler.load_middleware(is_async=is_async)

    assert len(base_handler._view_middleware) == 1
    assert len(base_handler._template_response_middleware) == 1
    assert len(base_handler._exception_middleware) == 1

def test_load_middleware_with_middleware_not_used(base_handler, settings, caplog):
    settings.MIDDLEWARE = [
        'path.to.TestMiddleware',
    ]
    
    with caplog.at_level(logging.DEBUG):
        base_handler.load_middleware(is_async=False)

    assert "MiddlewareNotUsed" in caplog.text

def test_load_middleware_with_invalid_middleware(base_handler, settings):
    settings.MIDDLEWARE = [
        'invalid.middleware.Path',
    ]

    with pytest.raises(ImproperlyConfigured):
        base_handler.load_middleware(is_async=False)

def test_load_middleware_without_sync_capable(base_handler, settings):
    class NonSyncCapableMiddleware:
        async_capable = False

        def __init__(self, get_response):
            self.get_response = get_response

    settings.MIDDLEWARE = [
        'path.to.NonSyncCapableMiddleware',
    ]
    
    with pytest.raises(RuntimeError):
        base_handler.load_middleware(is_async=False)