import pytest
from django.contrib.auth.models import User
from django.urls.resolvers import ResolverMatch

def test_repr():
    user = User(username='testuser', password='password')
    user.save()

    func_path = 'my_app.views.my_view'
    args = (1, 2, 3)
    kwargs = {'key': 'value'}
    url_name = 'my_url_name'
    app_names = ['my_app']
    namespaces = ['my_namespace']
    route = '/my/route/'

    match = ResolverMatch(func=func_path, args=args, kwargs=kwargs, url_name=url_name, app_names=app_names, namespaces=namespaces, route=route)

    expected_repr = "ResolverMatch(func=%s, args=%s, kwargs=%s, url_name=%s, app_names=%s, namespaces=%s, route=%s)" % (
        func_path, args, kwargs, url_name, app_names, namespaces, route
    )

    assert repr(match) == expected_repr