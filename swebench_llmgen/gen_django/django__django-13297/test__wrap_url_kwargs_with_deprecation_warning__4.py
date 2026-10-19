import pytest
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import User
from django.views.generic.base import _wrap_url_kwargs_with_deprecation_warning

def test_wrap_url_kwargs_with_deprecation_warning(caplog):
    url_kwargs = {'key1': 'value1', 'key2': 'value2'}
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        context_kwargs = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)

        # Check the keys in the returned context_kwargs
        assert 'key1' in context_kwargs
        assert 'key2' in context_kwargs

        # Access the values to trigger the deprecation warning
        assert context_kwargs['key1']() == 'value1'
        assert context_kwargs['key2']() == 'value2'

        # Check for the deprecation warnings
        assert len(w) == 2
        assert issubclass(w[0].category, RemovedInDjango40Warning)
        assert 'TemplateView passing URL kwargs to the context is deprecated' in str(w[0].message)

        assert issubclass(w[1].category, RemovedInDjango40Warning)
        assert 'TemplateView passing URL kwargs to the context is deprecated' in str(w[1].message)

    # Ensure the SimpleLazyObject is functioning correctly
    assert isinstance(context_kwargs['key1'], SimpleLazyObject)
    assert isinstance(context_kwargs['key2'], SimpleLazyObject)