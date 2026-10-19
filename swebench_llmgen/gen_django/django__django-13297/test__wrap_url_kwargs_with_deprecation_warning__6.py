import warnings
import pytest
from django.contrib.auth.models import User
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject

# Assuming the focal function is available in the current module
from django.views.generic.base import _wrap_url_kwargs_with_deprecation_warning

def test_wrap_url_kwargs_with_deprecation_warning():
    url_kwargs = {'user_id': 1, 'username': 'testuser'}

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # Trigger all warnings
        context_kwargs = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)

        # Access the values to trigger the warnings
        assert context_kwargs['user_id'].value == 1
        assert context_kwargs['username'].value == 'testuser'

        # Check if the appropriate warnings were raised
        assert len(w) == 2  # One for each key in url_kwargs
        assert issubclass(w[0].category, RemovedInDjango40Warning)
        assert 'TemplateView passing URL kwargs to the context is deprecated' in str(w[0].message)
        assert 'user_id' in str(w[0].message)
        assert issubclass(w[1].category, RemovedInDjango40Warning)
        assert 'TemplateView passing URL kwargs to the context is deprecated' in str(w[1].message)
        assert 'username' in str(w[1].message)

        # Check each key is a SimpleLazyObject instance
        for key in url_kwargs:
            assert isinstance(context_kwargs[key], SimpleLazyObject)