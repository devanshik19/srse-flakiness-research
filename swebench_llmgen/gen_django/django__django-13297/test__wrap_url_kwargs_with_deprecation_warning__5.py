import pytest
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject
from your_module_path import _wrap_url_kwargs_with_deprecation_warning  # Adjust the import path accordingly

def test_wrap_url_kwargs_with_deprecation_warning(caplog):
    url_kwargs = {'key1': 'value1', 'key2': 'value2'}
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        
        context_kwargs = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)
        
        # Verify the warning was triggered for each key
        assert len(w) == 2
        assert all(issubclass(w[i].category, RemovedInDjango40Warning) for i in range(2))
        assert 'TemplateView passing URL kwargs to the context is deprecated.' in str(w[0].message)
        assert 'TemplateView passing URL kwargs to the context is deprecated.' in str(w[1].message)

    # Test if the context returns the expected values
    assert context_kwargs['key1']() == 'value1'
    assert context_kwargs['key2']() == 'value2'