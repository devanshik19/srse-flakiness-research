import pytest
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from django.core.handlers.base import BaseHandler
from django.utils.module_loading import import_string
from unittest.mock import MagicMock

class MockMiddleware:
    sync_capable = True
    async_capable = False

    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

class AsyncMockMiddleware:
    sync_capable = False
    async_capable = True

    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, request):
        return None

def test_load_middleware_default_sync(monkeypatch):
    settings.MIDDLEWARE = [
        'path.to.MockMiddleware',
    ]
    monkeypatch.setattr('django.core.handlers.base.import_string', lambda path: MockMiddleware)

    handler = BaseHandler()
    handler.load_middleware()

    assert isinstance(handler._view_middleware[0], types.FunctionType)
    assert isinstance(handler._middleware_chain, types.FunctionType)
    assert handler._template_response_middleware == []
    assert handler._exception_middleware == []

def test_load_middleware_with_async(monkeypatch):
    settings.MIDDLEWARE = [
        'path.to.AsyncMockMiddleware',
    ]
    monkeypatch.setattr('django.core.handlers.base.import_string', lambda path: AsyncMockMiddleware)

    handler = BaseHandler()
    handler.load_middleware(is_async=True)

    assert isinstance(handler._view_middleware[0], types.FunctionType)
    assert isinstance(handler._middleware_chain, types.FunctionType)
    assert handler._template_response_middleware == []
    assert handler._exception_middleware == []

def test_load_middleware_invalid_middleware(monkeypatch):
    settings.MIDDLEWARE = [
        'path.to.InvalidMiddleware',
    ]
    monkeypatch.setattr('django.core.handlers.base.import_string', lambda path: None)

    handler = BaseHandler()
    
    with pytest.raises(ImproperlyConfigured):
        handler.load_middleware()

def test_load_middleware_raises_on_unusable(monkeypatch):
    class UnusableMiddleware:
        sync_capable = False
        async_capable = False
        
    settings.MIDDLEWARE = [
        'path.to.UnusableMiddleware',
    ]
    
    monkeypatch.setattr('django.core.handlers.base.import_string', lambda path: UnusableMiddleware)

    handler = BaseHandler()

    with pytest.raises(RuntimeError):
        handler.load_middleware()