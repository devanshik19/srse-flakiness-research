import pytest
import re
from django.urls.resolvers import RegexPattern

@pytest.fixture
def regex_pattern():
    pattern = r'^(?P<username>[\w-]+)/$'
    return RegexPattern(re.compile(pattern), name='user_profile', is_endpoint=False)

def test_match_with_named_groups(regex_pattern):
    path = 'john_doe/'
    remaining_path, args, kwargs = regex_pattern.match(path)
    assert remaining_path == ''
    assert args == ()
    assert kwargs == {'username': 'john_doe'}

def test_match_with_no_groups(regex_pattern):
    path = 'random/'
    remaining_path, args, kwargs = regex_pattern.match(path)
    assert remaining_path is None
    assert args == ()
    assert kwargs == {}

def test_match_with_extra_characters(regex_pattern):
    path = 'john_doe/something_else/'
    remaining_path, args, kwargs = regex_pattern.match(path)
    assert remaining_path == '/something_else/'
    assert args == ()
    assert kwargs == {'username': 'john_doe'}

def test_match_with_non_matching_path(regex_pattern):
    path = 'non_matching_text'
    result = regex_pattern.match(path)
    assert result is None