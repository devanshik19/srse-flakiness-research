import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import refs_expression

def test_refs_expression():
    # Setup annotations for the test
    user = User.objects.create(username='testuser')
    annotations = {
        'username': user.username,
        'user__nickname': 'Test Nickname'
    }
    
    # Test case where lookup_parts directly match annotations
    lookup_parts = ['username']
    result = refs_expression(lookup_parts, annotations)
    assert result == (user.username, [])

    # Test case where lookup_parts contain a prefix that matches annotations
    lookup_parts = ['user', 'nickname']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('Test Nickname', [])

    # Test case where lookup_parts contain no matches
    lookup_parts = ['email']
    result = refs_expression(lookup_parts, annotations)
    assert result == (False, ())

    # Test case with multiple elements in lookup_parts
    lookup_parts = ['user', 'nickname', 'extra']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('Test Nickname', ['extra'])

    # Test case where lookup_parts matches an empty annotations entry
    annotations_empty = {
        'username': user.username,
        'user__nickname': ''
    }
    lookup_parts = ['user', 'nickname']
    result = refs_expression(lookup_parts, annotations_empty)
    assert result == ('', [])

    # Test mixed cases with empty/falsey values in annotations
    annotations_mixed = {
        'username': user.username,
        'user__nickname': None
    }
    lookup_parts = ['user', 'nickname']
    result = refs_expression(lookup_parts, annotations_mixed)
    assert result == (None, [])