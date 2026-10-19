import pytest
from django.contrib.auth.models import User
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import refs_expression

def test_refs_expression():
    # Given annotations with a specific structure
    annotations = {
        'user': User,
        'user__username': 'username_annotation',
        'user__email': 'email_annotation',
    }
    
    # Test Case 1: Matching the exact lookup part
    lookup_parts_1 = ['user__username']
    result_1, remaining_1 = refs_expression(lookup_parts_1, annotations)
    assert result_1 == 'username_annotation'
    assert remaining_1 == []

    # Test Case 2: Matching a prefix with additional parts
    lookup_parts_2 = ['user', 'username']
    result_2, remaining_2 = refs_expression(lookup_parts_2, annotations)
    assert result_2 == User
    assert remaining_2 == ['username']

    # Test Case 3: No match found in annotations
    lookup_parts_3 = ['user__nonexistent']
    result_3, remaining_3 = refs_expression(lookup_parts_3, annotations)
    assert result_3 is False
    assert remaining_3 == ()

    # Test Case 4: Multiple matches in annotations
    lookup_parts_4 = ['user__email', 'extra']
    result_4, remaining_4 = refs_expression(lookup_parts_4, annotations)
    assert result_4 == 'email_annotation'
    assert remaining_4 == ['extra']

    # Test Case 5: Empty lookup parts
    lookup_parts_5 = []
    result_5, remaining_5 = refs_expression(lookup_parts_5, annotations)
    assert result_5 is False
    assert remaining_5 == ()