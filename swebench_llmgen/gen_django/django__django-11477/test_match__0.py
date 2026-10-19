import pytest
import re
from django.urls.resolvers import RegexPattern

@pytest.fixture
def regex_pattern():
    regex = re.compile(r'^(?P<username>\w+)/(?P<id>\d+)$')
    return RegexPattern(regex, 'test_view', False)

def test_match_with_named_groups(regex_pattern):
    path = "john/123"
    remaining_path, args, kwargs = regex_pattern.match(path)
    assert remaining_path == ""
    assert args == ()
    assert kwargs == {'username': 'john', 'id': '123'}

def test_match_without_named_groups(regex_pattern):
    regex = re.compile(r'^/(\d+)$')
    regex_pattern.regex = regex
    path = "/456"
    remaining_path, args, kwargs = regex_pattern.match(path)
    assert remaining_path == ""
    assert args == ('456',)
    assert kwargs == {}

def test_match_no_match(regex_pattern):
    path = "invalid_path"
    result = regex_pattern.match(path)
    assert result is None

def test_match_partial_match(regex_pattern):
    path = "john/"
    result = regex_pattern.match(path)
    assert result is None