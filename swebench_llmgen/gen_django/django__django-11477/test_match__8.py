import pytest
import re
from django.urls.resolvers import RegexPattern

@pytest.fixture
def regex_pattern():
    regex = re.compile(r'^(?P<username>[\w-]+)/(?P<action>[\w-]+)$')
    return RegexPattern(regex, 'test_pattern', False)

def test_match_with_named_groups(regex_pattern):
    path = 'john_doe/edit'
    remaining_path, args, kwargs = regex_pattern.match(path)
    
    assert remaining_path == ''
    assert args == ()
    assert kwargs == {'username': 'john_doe', 'action': 'edit'}

def test_match_without_named_groups(regex_pattern):
    regex_pattern.regex = re.compile(r'^(?P<username>[\w-]+)/(\w+)$')
    path = 'john_doe/view'
    remaining_path, args, kwargs = regex_pattern.match(path)
    
    assert remaining_path == ''
    assert args == ['view']
    assert kwargs == {'username': 'john_doe'}

def test_match_no_match(regex_pattern):
    path = 'non_matching_path'
    result = regex_pattern.match(path)
    
    assert result is None