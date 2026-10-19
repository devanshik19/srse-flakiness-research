import pytest
from django.core.handlers.base import BaseHandler
from django.conf import settings
import logging

# Prepare a sample middleware for testing
class SampleMiddleware:
    async_capable = True
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return None


@pytest.fixture
def settings_with_middleware(settings):
    settings.MIDDLEWARE = [
        'path.to.SampleMiddleware',  # Update with the correct import path
    ]


def test_load_middleware_sync(settings_with_middleware):
    handler = BaseHandler()
    handler.load_middleware(is_async=False)

    assert len(handler._view_middleware) == 1
    assert len(handler._template_response_middleware) == 1
    assert len(handler._exception_middleware) == 1
    assert handler._middleware_chain is not None


def test_load_middleware_async(settings_with_middleware):
    handler = BaseHandler()
    handler.load_middleware(is_async=True)

    assert len(handler._view_middleware) == 1
    assert len(handler._template_response_middleware) == 1
    assert len(handler._exception_middleware) == 1
    assert handler._middleware_chain is not None


def test_load_middleware_with_middleware_not_used(settings):
    class MiddlewareNotUsedSample:
        async_capable = False
        sync_capable = True

        def __init__(self, get_response):
            raise MiddlewareNotUsed("This middleware is not used")

    settings.MIDDLEWARE = [
        'path.to.MiddlewareNotUsedSample',  # Update with the correct import path
    ]
    
    handler = BaseHandler()
    handler.load_middleware(is_async=False)

    assert len(handler._view_middleware) == 0
    assert len(handler._template_response_middleware) == 0
    assert len(handler._exception_middleware) == 0
    assert handler._middleware_chain is not None


def test_load_middleware_improperly_configured(settings):
    class ImproperMiddleware:
        sync_capable = False
        async_capable = False

        def __init__(self, get_response):
            pass

    settings.MIDDLEWARE = [
        'path.to.ImproperMiddleware',  # Update with the correct import path
    ]

    handler = BaseHandler()

    with pytest.raises(RuntimeError) as excinfo:
        handler.load_middleware(is_async=False)
    assert "must have at least one of sync_capable/async_capable set to True." in str(excinfo.value)