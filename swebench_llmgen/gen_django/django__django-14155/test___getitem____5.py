import pytest
from django.contrib.auth.models import User
from django.urls.resolvers import ResolverMatch

def test_resolver_match_getitem():
    # Create a sample function to use in ResolverMatch
    def sample_view(request, *args, **kwargs):
        return "Sample Response"

    # Initialize ResolverMatch with the sample_view and some example args/kwargs
    func = sample_view
    args = (1, 2, 3)
    kwargs = {'key': 'value'}
    url_name = 'sample'
    app_names = ['app1']
    namespaces = ['namespace1']
    route = '/sample/'

    resolver_match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route, [])

    # Test __getitem__ with index 0
    result_func = resolver_match[0]
    assert result_func is func

    # Test __getitem__ with index 1
    result_args = resolver_match[1]
    assert result_args == args

    # Test __getitem__ with index 2
    result_kwargs = resolver_match[2]
    assert result_kwargs == kwargs

    # Test IndexError for out-of-bounds access
    with pytest.raises(IndexError):
        _ = resolver_match[3]