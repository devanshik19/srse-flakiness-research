import pytest
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject
from django.views.generic.base import _wrap_url_kwargs_with_deprecation_warning

def test_wrap_url_kwargs_with_deprecation_warning(monkeypatch):
    # Prepare test data
    url_kwargs = {
        'param1': 'value1',
        'param2': 'value2',
    }

    # Warnings capture
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # Always trigger the warning

        # Call the function
        context_kwargs = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)

        # Evaluate warnings for each key access
        for key in url_kwargs.keys():
            context_kwargs[key]()  # Trigger the SimpleLazyObject

        # Check warnings
        assert len(w) == len(url_kwargs)
        for key in url_kwargs.keys():
            assert issubclass(w[-1].category, RemovedInDjango40Warning)
            assert 'deprecated' in str(w[-1].message)
            assert key in str(w[-1].message)
            
    # Check the context_kwargs values
    assert context_kwargs['param1']() == 'value1'
    assert context_kwargs['param2']() == 'value2'