import warnings
import pytest
from django.contrib.auth.models import User
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject

from django.views.generic.base import _wrap_url_kwargs_with_deprecation_warning

@pytest.mark.parametrize("url_kwargs, expected_value", [
    ({"key1": "value1", "key2": "value2"}, ["value1", "value2"]),
    ({"foo": "bar"}, ["bar"]),
])
def test_wrap_url_kwargs_with_deprecation_warning(url_kwargs, expected_value):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        result = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)

        # Check if the warnings are raised
        assert len(w) == len(url_kwargs)
        for key in url_kwargs:
            assert issubclass(w[-1].category, RemovedInDjango40Warning)
            assert 'TemplateView passing URL kwargs to the context is deprecated' in str(w[-1].message)

        # Check if the returned values are accessible
        assert [result[key] for key in url_kwargs] == expected_value
        for key in url_kwargs:
            assert result[key]() == url_kwargs[key]

        # Ensure the access_value function is a SimpleLazyObject
            assert isinstance(result[key], SimpleLazyObject)