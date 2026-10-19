import pytest
from django.contrib.auth.models import User
from django.urls.resolvers import ResolverMatch

def test_resolver_match_repr():
    # Given
    user = User(username='testuser')
    func = 'myapp.views.test_view'
    args = (user,)
    kwargs = {'param': 'value'}
    url_name = 'test_url'
    app_names = ['myapp']
    namespaces = ['namespace1']
    route = '/test-route/'

    matcher = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route)

    # When
    repr_output = repr(matcher)

    # Then
    expected_repr = (
        "ResolverMatch(func=%s, args=%s, kwargs=%s, url_name=%s, "
        "app_names=%s, namespaces=%s, route=%s)" % (
            matcher._func_path, matcher.args, matcher.kwargs, matcher.url_name,
            matcher.app_names, matcher.namespaces, matcher.route,
        )
    )

    assert repr_output == expected_repr