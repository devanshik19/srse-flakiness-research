import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import refs_expression

def test_refs_expression():
    # Test Case 1: Lookup parts match annotations
    annotations = {
        'user': 'User annotation',
        'user__profile': 'User profile annotation',
    }
    lookup_parts = ['user', 'profile']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('User annotation', ['profile'])

    # Test Case 2: Partial match on lookup parts
    lookup_parts = ['user__profile']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('User profile annotation', [])

    # Test Case 3: No match in annotations
    lookup_parts = ['product']
    result = refs_expression(lookup_parts, annotations)
    assert result == (False, ())

    # Test Case 4: Lookup parts have no corresponding annotations (prefix matches)
    lookup_parts = ['user__nonexistent']
    result = refs_expression(lookup_parts, annotations)
    assert result == (False, ())

    # Test Case 5: Empty lookup parts
    lookup_parts = []
    result = refs_expression(lookup_parts, annotations)
    assert result == (False, ())