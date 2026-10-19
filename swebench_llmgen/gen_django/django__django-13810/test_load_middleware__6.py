import pytest
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from django.utils.module_loading import import_string
from django.contrib.auth.models import User
from django.core.handlers.base import BaseHandler


class DummyMiddleware:
    async_capable = True
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None


class AsyncDummyMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response

    async def process_view(self, request, view_func, view_args, view_kwargs):
        return None


class NonCapableMiddleware:
    async_capable = False
    sync_capable = False


@pytest.fixture(autouse=True)
def set_middleware_settings(settings):
    settings.MIDDLEWARE = [
        'path.to.DummyMiddleware',
        'path.to.AsyncDummyMiddleware',
    ]


def test_load_sync_middleware():
    handler = BaseHandler()
    handler.load_middleware(is_async=False)
    
    assert len(handler._view_middleware) == 1
    assert len(handler._template_response_middleware) == 0
    assert len(handler._exception_middleware) == 0
    assert handler._middleware_chain is not None


def test_load_async_middleware():
    handler = BaseHandler()
    handler.load_middleware(is_async=True)
    
    assert len(handler._view_middleware) == 1
    assert len(handler._template_response_middleware) == 0
    assert len(handler._exception_middleware) == 0
    assert handler._middleware_chain is not None


def test_load_non_capable_middleware():
    settings.MIDDLEWARE.append('path.to.NonCapableMiddleware')
    handler = BaseHandler()
    
    with pytest.raises(RuntimeError, match="Middleware path.to.NonCapableMiddleware must have at least one of sync_capable/async_capable set to True."):
        handler.load_middleware(is_async=False)

    with pytest.raises(RuntimeError, match="Middleware path.to.NonCapableMiddleware must have at least one of sync_capable/async_capable set to True."):
        handler.load_middleware(is_async=True)


def test_load_middleware_not_used():
    class DummyMiddlewareNotUsed:
        async_capable = True
        sync_capable = True

        def __init__(self, get_response):
            raise MiddlewareNotUsed("Not used")
    
    settings.MIDDLEWARE.append('path.to.DummyMiddlewareNotUsed')
    handler = BaseHandler()

    handler.load_middleware(is_async=False)
    # The previous middleware should still be in place
    assert len(handler._view_middleware) == 1