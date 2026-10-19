import pytest
from django.contrib.auth.models import User
from django.urls import ResolverMatch

def test_repr():
    user = User(username='testuser')
    user.save()
    
    f = lambda x: x  # Some dummy function to represent 'func'
    args = (user,)
    kwargs = {'attr': 'value'}
    url_name = 'test_url'
    app_names = ['app_name']
    namespaces = ['namespace']
    route = '/test/route/'
    
    match = ResolverMatch(func=f, args=args, kwargs=kwargs, url_name=url_name, app_names=app_names, namespaces=namespaces, route=route)
    
    expected_repr = f"ResolverMatch(func={f}, args=({user},), kwargs={{'attr': 'value'}}, url_name={url_name}, app_names={app_names}, namespaces={namespaces}, route={route})"
    
    assert repr(match) == expected_repr