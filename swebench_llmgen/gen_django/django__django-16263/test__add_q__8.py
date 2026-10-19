import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

def test_add_q_with_basic_conditions():
    query = Query(User)
    
    # Set up Q objects
    q1 = Q(username='testuser')
    q2 = Q(email='test@example.com')
    
    used_aliases = set()
    branch_negated = False
    current_negated = False
    allow_joins = True
    split_subq = True
    check_filterable = True
    
    # Test adding a single Q object
    target_clause, needed_inner = query._add_q(q1, used_aliases, branch_negated, current_negated, allow_joins, split_subq, check_filterable)
    
    assert target_clause.connector == 'AND'  # Check if the connector is correct.
    assert len(target_clause.children) == 1  # Check that one child is added.
    
    # Test adding multiple Q objects
    target_clause2, needed_inner2 = query._add_q(q2, used_aliases, branch_negated, current_negated, allow_joins, split_subq, check_filterable)
    
    assert len(target_clause2.children) == 1  # Check that the second clause is added.
    assert target_clause2.connector == 'AND'  # Check that the connector remained 'AND'.
    
    # Combine two clauses
    target_clause.add(target_clause2.children[0], target_clause.connector)
    assert len(target_clause.children) == 2  # Now it should have two children.
    
    # Check negation
    q3 = Q(is_active=False)
    branch_negated = True
    
    target_clause3, needed_inner3 = query._add_q(q3, used_aliases, branch_negated, current_negated, allow_joins, split_subq, check_filterable)
    
    assert target_clause3.negated is True  # Check if negated status is propagated correctly.
    assert len(target_clause3.children) == 1  # Ensure that only one child is added.