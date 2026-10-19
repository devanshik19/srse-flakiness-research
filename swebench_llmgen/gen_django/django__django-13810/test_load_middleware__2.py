import pytest
from django.conf import settings
from django.core.handlers.base import BaseHandler
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from unittest.mock import patch, MagicMock

@pytest.fixture
def base_handler():
    return BaseHandler()

def test_load_middleware_sync(base_handler):
    settings.MIDDLEWARE = [
        'django.middleware.common.CommonMiddleware',  # Example middleware
    ]
    
    # Patching the import_string to return a mock middleware
    with patch('django.utils.module_loading.import_string') as mock_import:
        mock_middleware = MagicMock()
        mock_middleware.sync_capable = True
        mock_middleware.async_capable = False
        mock_import.return_value = mock_middleware

        base_handler.load_middleware(is_async=False)

        assert len(base_handler._view_middleware) == 1
        assert len(base_handler._template_response_middleware) == 0
        assert len(base_handler._exception_middleware) == 0
        assert base_handler._middleware_chain is not None

def test_load_middleware_async(base_handler):
    settings.MIDDLEWARE = [
        'django.middleware.common.CommonMiddleware',  # Example middleware
    ]

    # Patching the import_string to return a mock middleware
    with patch('django.utils.module_loading.import_string') as mock_import:
        mock_middleware = MagicMock()
        mock_middleware.sync_capable = True
        mock_middleware.async_capable = True
        mock_import.return_value = mock_middleware

        base_handler.load_middleware(is_async=True)

        assert len(base_handler._view_middleware) == 1
        assert len(base_handler._template_response_middleware) == 0
        assert len(base_handler._exception_middleware) == 0
        assert base_handler._middleware_chain is not None

def test_load_middleware_middleware_not_used(base_handler):
    settings.MIDDLEWARE = [
        'django.middleware.common.CommonMiddleware',  # Example middleware
    ]
    
    with patch('django.utils.module_loading.import_string') as mock_import:
        mock_middleware = MagicMock(side_effect=MiddlewareNotUsed("Middleware not used"))
        mock_import.return_value = mock_middleware

        base_handler.load_middleware(is_async=False)
        assert len(base_handler._view_middleware) == 0

def test_load_middleware_improperly_configured(base_handler):
    settings.MIDDLEWARE = [
        'django.middleware.common.CommonMiddleware',  # Example middleware
    ]

    with patch('django.utils.module_loading.import_string') as mock_import:
        mock_middleware = MagicMock()
        mock_middleware.sync_capable = False
        mock_middleware.async_capable = False
        mock_import.return_value = mock_middleware

        with pytest.raises(RuntimeError, match="must have at least one of sync_capable/async_capable set to True"):
            base_handler.load_middleware(is_async=False)