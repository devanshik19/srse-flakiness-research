import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_add_q():
    query = Query(User)
    used_aliases = set()
    
    # Create Q objects with multiple scenarios
    q1 = Q(username='testuser1')
    q2 = Q(username='testuser2', negated=True)
    
    # Test case 1: Basic Q object addition
    target_clause1, needed_inner1 = query._add_q(q1, used_aliases)
    assert len(target_clause1.children) == 1
    
    # Test case 2: Negated Q object addition
    target_clause2, needed_inner2 = query._add_q(q2, used_aliases)
    assert len(target_clause2.children) == 1
    
    # Test case 3: Combine multiple Q objects
    combined_q = q1 & q2
    target_clause3, needed_inner3 = query._add_q(combined_q, used_aliases)
    assert len(target_clause3.children) == 2  # should have both conditions
    
    # Test case 4: Check branching with negation
    negated_q = Q(username='testuser3', negated=True)
    target_clause4, needed_inner4 = query._add_q(negated_q, used_aliases, branch_negated=True)
    assert len(target_clause4.children) == 1
    assert target_clause4.negated is True
    
    # Ensure no side effects on query structure
    assert len(query.where.children) == 0  # Original query should remain unchanged

    # Test with allow_joins as False
    target_clause5, needed_inner5 = query._add_q(q1, used_aliases, allow_joins=False)
    assert len(target_clause5.children) == 1