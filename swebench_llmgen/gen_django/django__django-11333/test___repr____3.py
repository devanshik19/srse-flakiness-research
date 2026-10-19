import pytest
from django.contrib.auth.models import User
from django.urls import ResolverMatch

def test_resolver_match_repr():
    user = User(username='testuser')
    user.save()
    
    args = (1, 2, 3)
    kwargs = {'key': 'value'}
    url_name = 'test_url'
    app_names = ['app1', 'app2']
    namespaces = ['namespace1', 'namespace2']
    route = 'test/route/'

    resolver_match = ResolverMatch(func=user, args=args, kwargs=kwargs, 
                                    url_name=url_name, app_names=app_names, 
                                    namespaces=namespaces, route=route)

    expected_repr = (
        "ResolverMatch(func=%s, args=%s, kwargs=%s, url_name=%s, "
        "app_names=%s, namespaces=%s, route=%s)" % (
            user.__repr__(), args, kwargs, url_name, 
            app_names, namespaces, route
        )
    )

    assert resolver_match.__repr__() == expected_repr