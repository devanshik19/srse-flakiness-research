import pytest
import warnings
from django.contrib.auth.models import User
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject
from django.urls import reverse

# Assuming the function _wrap_url_kwargs_with_deprecation_warning is imported from the correct module path
from django.views.generic.base import _wrap_url_kwargs_with_deprecation_warning

def test_wrap_url_kwargs_with_deprecation_warning(caplog):
    # Prepare test data
    url_kwargs = {
        'key1': 'value1',
        'key2': 'value2'
    }

    # Call the function
    context_kwargs = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)

    # Access the values to trigger the warning
    value1 = context_kwargs['key1']
    value2 = context_kwargs['key2']

    # Assert that the warning was issued
    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[0].message == (
        'TemplateView passing URL kwargs to the context is deprecated. '
        'Reference key1 in your template through view.kwargs instead.'
    )
    assert caplog.records[1].levelname == 'WARNING'
    assert caplog.records[1].message == (
        'TemplateView passing URL kwargs to the context is deprecated. '
        'Reference key2 in your template through view.kwargs instead.'
    )

    # Assert that the values are correct
    assert value1 == 'value1'
    assert value2 == 'value2'