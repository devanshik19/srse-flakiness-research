import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import MiddlewareNotUsed
from django.utils.module_loading import import_string
from django.core.handlers.base import BaseHandler
from .exception import convert_exception_to_response

# Sample middleware for testing
class TestMiddleware:
    async_capable = True
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

# Update settings for testing
settings.MIDDLEWARE = [
    'path.to.TestMiddleware',  # Adjust the path as needed
]

@pytest.mark.django_db
def test_load_middleware_sync():
    handler = BaseHandler()
    handler.load_middleware(is_async=False)
    assert len(handler._view_middleware) == 1
    assert isinstance(handler._view_middleware[0], types.FunctionType)

@pytest.mark.django_db
def test_load_middleware_async():
    handler = BaseHandler()
    handler.load_middleware(is_async=True)
    assert len(handler._view_middleware) == 1
    assert isinstance(handler._view_middleware[0], types.FunctionType)

def test_load_middleware_invalid_sync_capability():
    settings.MIDDLEWARE.append('path.to.InvalidMiddleware')

    class InvalidMiddleware:
        async_capable = False
        sync_capable = False

        def __init__(self, get_response):
            self.get_response = get_response

    handler = BaseHandler()
    with pytest.raises(RuntimeError, match='must have at least one of'):
        handler.load_middleware(is_async=False)

def test_load_middleware_middleware_not_used():
    settings.MIDDLEWARE.append('path.to.NotUsedMiddleware')

    class NotUsedMiddleware:
        async_capable = True
        sync_capable = True

        def __init__(self, get_response):
            raise MiddlewareNotUsed('Not used')

    handler = BaseHandler()
    handler.load_middleware(is_async=False)
    assert len(handler._view_middleware) == 0  # Ensure it skipped the middleware