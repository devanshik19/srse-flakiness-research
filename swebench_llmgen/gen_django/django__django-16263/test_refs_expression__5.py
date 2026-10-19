import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import refs_expression

def test_refs_expression():
    annotations = {
        'name': 'name_annotation',
        'email': 'email_annotation',
        'profile__age': 'age_annotation',
        'profile__city': 'city_annotation',
    }

    # Test case 1: Lookup with existing annotation
    lookup_parts = ['profile', 'age']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('age_annotation', ['city'])

    # Test case 2: Lookup with no matching annotation
    lookup_parts = ['profile', 'nonexistent']
    result = refs_expression(lookup_parts, annotations)
    assert result == (False, ())

    # Test case 3: Lookup with multiple valid prefixes
    lookup_parts = ['name', 'extra']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('name_annotation', ['extra'])

    # Test case 4: Lookup that matches the last key
    lookup_parts = ['profile', 'city']
    result = refs_expression(lookup_parts, annotations)
    assert result == ('city_annotation', [])

    # Test case 5: Empty lookup_parts
    lookup_parts = []
    result = refs_expression(lookup_parts, annotations)
    assert result == (False, ())