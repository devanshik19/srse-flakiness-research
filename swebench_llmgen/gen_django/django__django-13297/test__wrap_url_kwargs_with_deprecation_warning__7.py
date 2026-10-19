import pytest
import warnings
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import User

def _wrap_url_kwargs_with_deprecation_warning(url_kwargs):
    context_kwargs = {}
    for key, value in url_kwargs.items():
        @SimpleLazyObject
        def access_value(key=key, value=value):
            warnings.warn(
                'TemplateView passing URL kwargs to the context is '
                'deprecated. Reference %s in your template through '
                'view.kwargs instead.' % key,
                RemovedInDjango40Warning, stacklevel=2,
            )
            return value
        context_kwargs[key] = access_value
    return context_kwargs

@pytest.mark.filterwarnings('ignore::django.utils.deprecation.RemovedInDjango40Warning')
def test_wrap_url_kwargs_with_deprecation_warning(caplog):
    url_kwargs = {'foo': 'bar', 'baz': 'qux'}
    result = _wrap_url_kwargs_with_deprecation_warning(url_kwargs)

    assert 'foo' in result
    assert 'baz' in result
    
    value_foo = result['foo']
    value_baz = result['baz']
    
    # Access the values to trigger the warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        assert value_foo() == 'bar'
        assert value_baz() == 'qux'
        
        assert len(w) == 2
        assert issubclass(w[0].category, RemovedInDjango40Warning)
        assert 'foo' in str(w[0].message)
        assert issubclass(w[1].category, RemovedInDjango40Warning)
        assert 'baz' in str(w[1].message)