import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from django.utils.module_loading import import_string
from django.core.handlers.base import BaseHandler

# Assuming there's a simple middleware for testing
class DummyMiddleware:
    async_capable = True
    sync_capable = True
    
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

# Add the middleware to settings for testing
settings.MIDDLEWARE = ['path.to.DummyMiddleware']

@pytest.fixture
def base_handler():
    return BaseHandler()

def test_load_middleware_sync(base_handler):
    base_handler.load_middleware(is_async=False)
    
    assert isinstance(base_handler._view_middleware, list)
    assert isinstance(base_handler._template_response_middleware, list)
    assert isinstance(base_handler._exception_middleware, list)
    assert len(base_handler._view_middleware) == 1
    assert len(base_handler._template_response_middleware) == 1
    assert len(base_handler._exception_middleware) == 1

def test_load_middleware_async(base_handler):
    base_handler.load_middleware(is_async=True)
    
    assert isinstance(base_handler._view_middleware, list)
    assert isinstance(base_handler._template_response_middleware, list)
    assert isinstance(base_handler._exception_middleware, list)
    assert len(base_handler._view_middleware) == 1
    assert len(base_handler._template_response_middleware) == 1
    assert len(base_handler._exception_middleware) == 1

def test_load_middleware_invalid(base_handler):
    settings.MIDDLEWARE.append('invalid.middleware.path')
    
    with pytest.raises(ImproperlyConfigured):
        base_handler.load_middleware(is_async=False)

def test_load_middleware_middleware_not_used(base_handler):
    class MiddlewareNotUsedDummy:
        async_capable = False
        sync_capable = True
        
        def __init__(self, get_response):
            raise MiddlewareNotUsed("This middleware is not used.")

    middleware_path = 'path.to.MiddlewareNotUsedDummy'
    settings.MIDDLEWARE.append(middleware_path)

    with pytest.raises(MiddlewareNotUsed):
        base_handler.load_middleware(is_async=False)

    assert len(base_handler._view_middleware) == 0
    assert len(base_handler._template_response_middleware) == 0
    assert len(base_handler._exception_middleware) == 0