import warnings
import pytest
from django.contrib.auth.models import User
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject

from django.views.generic.base import _wrap_url_kwargs_with_deprecation_warning


def test_wrap_url_kwargs_with_deprecation_warning(caplog):
    url_kwargs = {'foo': 'bar', 'baz': 'qux'}
    context_kwargs = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)

    assert 'foo' in context_kwargs
    assert 'baz' in context_kwargs

    # Accessing the wrapped values should trigger a warning
    with caplog.at_level(logging.WARNING):
        context_kwargs['foo']()
        context_kwargs['baz']()

    # Check if the correct deprecation warning was issued
    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == "WARNING"
    assert isinstance(caplog.records[0].message, str)
    assert "deprecated" in caplog.records[0].message
    assert "foo" in caplog.records[0].message

    assert caplog.records[1].levelname == "WARNING"
    assert isinstance(caplog.records[1].message, str)
    assert "deprecated" in caplog.records[1].message
    assert "baz" in caplog.records[1].message

    # Validate the values returned
    assert context_kwargs['foo']() == 'bar'
    assert context_kwargs['baz']() == 'qux'