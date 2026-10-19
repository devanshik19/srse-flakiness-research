import pytest
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from django.utils.module_loading import import_string
from django.contrib.auth.models import User
from django.urls import get_resolver
from django.core.handlers.base import BaseHandler

class TestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return None

def test_load_middleware_sync(monkeypatch):
    monkeypatch.setattr('django.conf.settings.MIDDLEWARE', [
        'path.to.TestMiddleware',
    ])
    
    handler = BaseHandler()
    handler.load_middleware(is_async=False)

    assert isinstance(handler._view_middleware[0], types.FunctionType)
    assert isinstance(handler._template_response_middleware[0], types.FunctionType)
    assert isinstance(handler._exception_middleware[0], types.FunctionType)

def test_load_middleware_async(monkeypatch):
    monkeypatch.setattr('django.conf.settings.MIDDLEWARE', [
        'path.to.TestMiddleware',
    ])
    
    handler = BaseHandler()
    handler.load_middleware(is_async=True)

    assert isinstance(handler._view_middleware[0], types.FunctionType)
    assert isinstance(handler._template_response_middleware[0], types.FunctionType)
    assert isinstance(handler._exception_middleware[0], types.FunctionType)

def test_load_middleware_middleware_not_used(monkeypatch, caplog):
    class NotUsedMiddleware:
        def __init__(self, get_response):
            raise MiddlewareNotUsed("This middleware is not used.")

    monkeypatch.setattr('django.conf.settings.MIDDLEWARE', [
        'path.to.NotUsedMiddleware',
    ])
    
    with caplog.at_level(logging.DEBUG):
        handler = BaseHandler()
        handler.load_middleware(is_async=False)

    assert "MiddlewareNotUsed" in caplog.text

def test_load_middleware_improperly_configured(monkeypatch):
    class ImproperMiddleware:
        def __init__(self, get_response):
            pass

    monkeypatch.setattr('django.conf.settings.MIDDLEWARE', [
        'path.to.ImproperMiddleware',
    ])
    
    with pytest.raises(ImproperlyConfigured):
        handler = BaseHandler()
        handler.load_middleware(is_async=False)

def test_load_middleware_sync_and_async(monkeypatch):
    class SyncMiddleware:
        sync_capable = True
        async_capable = False

        def __init__(self, get_response):
            self.get_response = get_response

        def process_view(self, request, view_func, view_args, view_kwargs):
            return None

    class AsyncMiddleware:
        sync_capable = False
        async_capable = True

        def __init__(self, get_response):
            self.get_response = get_response

        async def process_view(self, request, view_func, view_args, view_kwargs):
            return None

    monkeypatch.setattr('django.conf.settings.MIDDLEWARE', [
        'path.to.SyncMiddleware',
        'path.to.AsyncMiddleware',
    ])
    
    handler = BaseHandler()
    handler.load_middleware(is_async=True)

    assert len(handler._view_middleware) == 2
    assert len(handler._template_response_middleware) == 0
    assert len(handler._exception_middleware) == 0