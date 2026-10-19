import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode
from django.db.models.sql.query import Query

def test_add_q_with_simple_q_object():
    query = Query(User)
    q_object = Q(username='testuser')
    used_aliases = {}
    
    # Call the _add_q method
    target_clause, needed_inner = query._add_q(q_object, used_aliases)

    # Check that the target_clause is not None
    assert target_clause is not None
    assert isinstance(target_clause, WhereNode)
    assert len(target_clause.children) == 1  # Expecting one child clause
    assert target_clause.connector == 'AND'  # Default connector

def test_add_q_with_negated_q_object():
    query = Query(User)
    q_object = Q(username='testuser', negated=True)
    used_aliases = {}

    # Call the _add_q method
    target_clause, needed_inner = query._add_q(q_object, used_aliases)

    # Check that the target_clause is correctly negated
    assert target_clause is not None
    assert target_clause.negated is True
    assert len(target_clause.children) == 1  # Expecting one child clause

def test_add_q_with_multiple_children():
    query = Query(User)
    q_object = Q(username='testuser') | Q(email='test@example.com')
    used_aliases = {}

    # Call the _add_q method
    target_clause, needed_inner = query._add_q(q_object, used_aliases)

    # Check that the target_clause has the correct number of children
    assert target_clause is not None
    assert len(target_clause.children) == 2  # Expecting two child clauses
    assert target_clause.connector == 'OR'  # Should reflect the connector from Q

def test_add_q_with_complex_q_object():
    query = Query(User)
    q_object = Q(username='testuser') & (Q(email='test@example.com') | Q(is_active=True))
    used_aliases = {}

    # Call the _add_q method
    target_clause, needed_inner = query._add_q(q_object, used_aliases)

    # Validate the structure of the resulting target_clause
    assert target_clause is not None
    assert len(target_clause.children) == 2  # One for username, one for the OR condition
    assert target_clause.connector == 'AND'  # Should be AND for the top level
    assert isinstance(target_clause.children[1], WhereNode)  # Second should be an OR node

def test_add_q_with_empty_q_object():
    query = Query(User)
    q_object = Q()  # Empty Q
    used_aliases = {}

    # Call the _add_q method
    target_clause, needed_inner = query._add_q(q_object, used_aliases)

    # Check that the target_clause is effectively empty
    assert target_clause is not None
    assert len(target_clause.children) == 0  # Expecting no child clauses