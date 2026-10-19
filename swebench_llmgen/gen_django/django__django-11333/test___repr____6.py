import pytest
from django.contrib.auth.models import User
from django.urls import ResolverMatch

@pytest.fixture
def resolver_match():
    user = User(username='testuser')
    user.save()
    return ResolverMatch(func='test_func', 
                          args=('arg1', 'arg2'), 
                          kwargs={'key': 'value'}, 
                          url_name='test_url', 
                          app_names=['app1', 'app2'], 
                          namespaces=['ns1', 'ns2'], 
                          route='/test/')

def test_repr(resolver_match):
    expected_repr = ("ResolverMatch(func=test_func, args=('arg1', 'arg2'), kwargs={'key': 'value'}, "
                     "url_name=test_url, app_names=['app1', 'app2'], namespaces=['ns1', 'ns2'], route=/test/)")
    assert repr(resolver_match) == expected_repr