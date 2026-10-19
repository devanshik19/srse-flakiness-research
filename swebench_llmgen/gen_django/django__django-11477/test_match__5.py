import pytest
import re
from django.urls.resolvers import RegexPattern

@pytest.fixture
def regex_pattern():
    pattern = re.compile(r'^(?P<name>\w+)/(?P<id>\d+)$')
    return RegexPattern(pattern, 'test_name', False)

def test_match_with_named_groups(regex_pattern):
    path = 'john/123'
    remaining, args, kwargs = regex_pattern.match(path)

    assert remaining == ''
    assert args == ()
    assert kwargs == {'name': 'john', 'id': '123'}

def test_match_with_no_named_groups(regex_pattern):
    path = 'john/123/extra'
    remaining, args, kwargs = regex_pattern.match(path)

    assert remaining == '/extra'
    assert args == ()
    assert kwargs == {'name': 'john', 'id': '123'}

def test_match_no_match(regex_pattern):
    path = 'unknown'
    result = regex_pattern.match(path)

    assert result is None