import pytest
from django.contrib.auth.models import User
from django.urls import ResolverMatch

def test_resolver_match_repr():
    user = User.objects.create(username='testuser')
    func = 'my_view_function'
    args = (user.id,)
    kwargs = {'foo': 'bar'}
    url_name = 'my_url_name'
    app_names = ['my_app']
    namespaces = ['my_namespace']
    route = '/my/url/'

    resolver_match = ResolverMatch(func=func, args=args, kwargs=kwargs, url_name=url_name, app_names=app_names, namespaces=namespaces, route=route)
    
    expected_repr = "ResolverMatch(func=%s, args=%s, kwargs=%s, url_name=%s, app_names=%s, namespaces=%s, route=%s)" % (
        func, args, kwargs, url_name, app_names, namespaces, route
    )
    
    assert repr(resolver_match) == expected_repr