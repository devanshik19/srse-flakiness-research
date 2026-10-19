import pytest
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject
from django.views.generic.base import _wrap_url_kwargs_with_deprecation_warning

def test_wrap_url_kwargs_with_deprecation_warning(caplog):
    url_kwargs = {'key1': 'value1', 'key2': 'value2'}
    context_kwargs = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)

    # Check that context_kwargs has the same keys
    assert context_kwargs.keys() == url_kwargs.keys()

    # Verify the values trigger a deprecation warning when accessed
    with caplog.at_level(logging.WARNING):
        value1 = context_kwargs['key1']()
        value2 = context_kwargs['key2']()
        
    # Check that the warning is issued
    assert len(caplog.records) == 2
    assert all("TemplateView passing URL kwargs to the context is deprecated" in rec.message for rec in caplog.records)
    assert all(rec.levelname == 'WARNING' for rec in caplog.records)

    # Verify that the values returned are as expected
    assert value1 == 'value1'
    assert value2 == 'value2'