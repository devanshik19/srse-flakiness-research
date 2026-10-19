import pytest
import re
from django.urls.resolvers import RegexPattern

@pytest.fixture
def regex_pattern():
    return RegexPattern(regex=re.compile(r'^(?P<id>\d+)/$'), name='test', is_endpoint=False)

def test_match_with_named_groups(regex_pattern):
    path = "123/"
    remaining_path, args, kwargs = regex_pattern.match(path)
    assert remaining_path == ""
    assert args == ()
    assert kwargs == {'id': '123'}

def test_match_with_no_named_groups(regex_pattern):
    regex_pattern.regex = re.compile(r'^(?P<id>\d+)/details/$')
    path = "123/details/"
    remaining_path, args, kwargs = regex_pattern.match(path)
    assert remaining_path == ""
    assert args == ()
    assert kwargs == {'id': '123'}

def test_match_no_match(regex_pattern):
    path = "abc/"
    result = regex_pattern.match(path)
    assert result is None

def test_match_empty_path(regex_pattern):
    path = ""
    result = regex_pattern.match(path)
    assert result is None

def test_match_with_extra_slashes(regex_pattern):
    path = "123///"
    result = regex_pattern.match(path)
    assert result is None