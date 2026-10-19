import pytest
import re
from django.urls.resolvers import RegexPattern

@pytest.fixture
def pattern():
    regex = re.compile(r'^(?P<username>\w+)/(?P<id>\d+)$')
    return RegexPattern(regex, name='user_detail', is_endpoint=True)

def test_match_with_named_groups(pattern):
    path = "john_doe/123"
    remaining_path, args, kwargs = pattern.match(path)
    assert remaining_path == ""
    assert args == ()
    assert kwargs == {'username': 'john_doe', 'id': '123'}

def test_match_with_no_named_groups(pattern):
    regex = re.compile(r'^(\w+)$')
    pattern.regex = regex
    path = "john_doe"
    remaining_path, args, kwargs = pattern.match(path)
    assert remaining_path == ""
    assert args == ('john_doe',)
    assert kwargs == {}

def test_match_with_no_match(pattern):
    path = "unknown_user"
    result = pattern.match(path)
    assert result is None