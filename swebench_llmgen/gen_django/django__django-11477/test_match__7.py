import pytest
import re
from django.urls.resolvers import RegexPattern

@pytest.fixture
def regex_pattern():
    # Create a RegexPattern instance with a sample regex that has named groups
    regex = re.compile(r'^(?P<slug>[\w-]+)/?$')
    return RegexPattern(regex, name='test', is_endpoint=False)

def test_match_with_named_groups(regex_pattern):
    path = 'example-slug/'
    expected_args = ()
    expected_kwargs = {'slug': 'example-slug'}
    remaining_path, args, kwargs = regex_pattern.match(path)
    
    assert remaining_path == ''
    assert args == expected_args
    assert kwargs == expected_kwargs

def test_match_without_named_groups(regex_pattern):
    path = 'example-slug'
    expected_args = ()
    expected_kwargs = {}
    remaining_path, args, kwargs = regex_pattern.match(path)
    
    assert remaining_path == ''
    assert args == expected_args
    assert kwargs == expected_kwargs

def test_match_no_match(regex_pattern):
    path = 'unmatched-path'
    result = regex_pattern.match(path)
    
    assert result is None