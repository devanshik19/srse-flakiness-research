import warnings
import pytest
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject
from django.views.generic.base import _wrap_url_kwargs_with_deprecation_warning

def test_wrap_url_kwargs_with_deprecation_warning(caplog):
    url_kwargs = {'foo': 'bar', 'baz': 'qux'}
    context_kwargs = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)

    assert 'foo' in context_kwargs
    assert 'baz' in context_kwargs

    with caplog.at_level(logging.WARNING):
        value_foo = context_kwargs['foo']()
        value_baz = context_kwargs['baz']()

    assert value_foo == 'bar'
    assert value_baz == 'qux'
    
    assert len(caplog.records) == 2
    assert caplog.records[0].message == (
        'TemplateView passing URL kwargs to the context is '
        'deprecated. Reference %s in your template through '
        'view.kwargs instead.' % 'foo'
    )
    assert caplog.records[1].message == (
        'TemplateView passing URL kwargs to the context is '
        'deprecated. Reference %s in your template through '
        'view.kwargs instead.' % 'baz'
    )

    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[1].levelname == 'WARNING'
    assert caplog.records[0].filename == 'base.py'
    assert caplog.records[1].filename == 'base.py'
    assert isinstance(caplog.records[0].message, str)
    assert isinstance(caplog.records[1].message, str)