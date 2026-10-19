import pytest
from django.contrib.auth.models import User
from django.urls.resolvers import ResolverMatch

def test_resolver_match_repr():
    # Arrange
    user = User(username='testuser')
    user.save()

    func = 'my_app.views.my_view'  # assuming this is a valid view path
    args = (user.id,)
    kwargs = {'extra': 'value'}
    url_name = 'my_url_name'
    app_names = ['my_app']
    namespaces = ['my_namespace']
    route = '/my/route/'

    resolver_match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route)

    # Act
    result = repr(resolver_match)

    # Assert
    expected_repr = (
        "ResolverMatch(func=%s, args=(%s,), kwargs=%s, url_name=%s, "
        "app_names=%s, namespaces=%s, route=%s)" % 
        (func, user.id, kwargs, url_name, app_names, namespaces, route)
    )
    assert result == expected_repr