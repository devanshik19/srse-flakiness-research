import pytest
from django.urls import RegexPattern


@pytest.fixture
def regex_pattern():
    return RegexPattern(regex=r'^(?P<username>[\w-]+)/$', name='profile', is_endpoint=False)


def test_match_with_named_groups(regex_pattern):
    path = 'john/'
    remaining, args, kwargs = regex_pattern.match(path)
    
    assert remaining == ''
    assert args == ()
    assert kwargs == {'username': 'john'}


def test_match_with_positional_groups(regex_pattern):
    # Modify the regex to include a positional group
    regex_pattern.regex = re.compile(r'^(?P<username>[\w-]+)/(?P<id>\d+)/$')
    
    path = 'john/123/'
    remaining, args, kwargs = regex_pattern.match(path)
    
    assert remaining == ''
    assert args == ()
    assert kwargs == {'username': 'john', 'id': '123'}


def test_match_no_match(regex_pattern):
    path = 'non_matching_path/'
    result = regex_pattern.match(path)
    
    assert result is None


def test_match_empty_path(regex_pattern):
    path = ''
    result = regex_pattern.match(path)
    
    assert result is None