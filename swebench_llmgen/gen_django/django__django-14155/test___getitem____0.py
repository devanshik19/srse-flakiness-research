import pytest
from django.contrib.auth.models import User
from django.urls import ResolverMatch

def test_getitem():
    # Create a dummy view function
    def dummy_view(request, *args, **kwargs):
        return "Dummy view"

    # Prepare test data
    args = (1, 2, 3)
    kwargs = {'key': 'value'}
    url_name = 'dummy_url'
    app_names = ['app1', 'app2']
    namespaces = ['namespace1', 'namespace2']
    route = '/dummy-route/'

    # Create an instance of ResolverMatch
    match = ResolverMatch(dummy_view, args, kwargs, url_name, app_names, namespaces, route, [])

    # Test the __getitem__ method for different indices
    func = match[0]
    args_returned = match[1]
    kwargs_returned = match[2]

    # Assertions
    assert func == dummy_view
    assert args_returned == args
    assert kwargs_returned == kwargs

    # Test out of range access
    with pytest.raises(IndexError):
        _ = match[3]