import pytest
import re
from django.urls.resolvers import RegexPattern

@pytest.fixture
def regex_pattern():
    # Create a RegexPattern instance with a simple regex
    pattern = RegexPattern(regex=re.compile(r'^(?P<name>\w+)/(?P<age>\d+)$'), name='test_view', is_endpoint=True)
    return pattern

def test_match_success_with_named_groups(regex_pattern):
    path = "john/30"
    remaining, args, kwargs = regex_pattern.match(path)
    
    assert remaining == ""
    assert args == ()
    assert kwargs == {"name": "john", "age": "30"}

def test_match_success_with_no_named_groups():
    pattern = RegexPattern(regex=re.compile(r'^(?P<id>\d+)/?$'), name='test_view', is_endpoint=True)
    path = "123"
    remaining, args, kwargs = pattern.match(path)
    
    assert remaining == ""
    assert args == ()
    assert kwargs == {"id": "123"}

def test_match_no_match(regex_pattern):
    path = "invalid_path"
    result = regex_pattern.match(path)
    
    assert result is None