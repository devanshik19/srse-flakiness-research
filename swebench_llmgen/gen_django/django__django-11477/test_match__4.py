import pytest
import re
from django.urls.resolvers import RegexPattern

@pytest.fixture
def regex_pattern():
    regex = re.compile(r'^(?P<slug>[\w-]+)/?$')
    return RegexPattern(regex, name='slug', is_endpoint=False)

def test_match_with_named_group(regex_pattern):
    path = 'test-slug/'
    expected_remaining_path = ''
    expected_args = ()
    expected_kwargs = {'slug': 'test-slug'}

    result = regex_pattern.match(path)
    
    assert result is not None
    assert result == (expected_remaining_path, expected_args, expected_kwargs)

def test_match_with_positional_group(regex_pattern):
    regex_pattern_with_positional = RegexPattern(re.compile(r'^(.*?)/?$'), name='any', is_endpoint=False)
    path = 'test-path/'
    expected_remaining_path = ''
    expected_args = ('test-path',)
    expected_kwargs = {}

    result = regex_pattern_with_positional.match(path)

    assert result is not None
    assert result == (expected_remaining_path, expected_args, expected_kwargs)

def test_match_no_match(regex_pattern):
    path = 'no-match-here/'

    result = regex_pattern.match(path)

    assert result is None