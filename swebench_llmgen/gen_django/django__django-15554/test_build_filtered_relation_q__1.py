import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode

def test_build_filtered_relation_q():
    # Create a new Query instance
    query = Query(model=None)

    # Create a simple Q object
    q_object = Q('username__exact', 'testuser') & Q('email__icontains', 'example.com')
    
    # Build the filtered relation Q
    result = query.build_filtered_relation_q(q_object, reuse=False)

    # Build expected WhereNode based on the Q object
    expected_connector = q_object.connector
    expected_clause = WhereNode(connector=expected_connector, negated=q_object.negated)
    
    # Manually add expected conditions
    for child in q_object.children:
        child_clause, _ = query.build_filter(child, allow_joins=True)
        expected_clause.add(child_clause, expected_connector)
    
    assert result == expected_clause

def test_build_filtered_relation_q_with_negation():
    query = Query(model=None)

    # Create a negated Q object
    q_object = Q('username__exact', 'testuser') | Q('email__icontains', 'example.com')
    
    # Build the filtered relation Q with negation
    result = query.build_filtered_relation_q(q_object, reuse=False, branch_negated=True)

    expected_connector = q_object.connector
    expected_clause = WhereNode(connector=expected_connector, negated=q_object.negated)

    for child in q_object.children:
        child_clause, _ = query.build_filter(child, allow_joins=True)
        expected_clause.add(child_clause, expected_connector)

    assert result == expected_clause

def test_build_filtered_relation_q_with_empty_children():
    query = Query(model=None)

    # Create an empty Q object
    q_object = Q()
    
    # Build the filtered relation Q with empty Q object
    result = query.build_filtered_relation_q(q_object, reuse=False)

    expected_connector = q_object.connector
    expected_clause = WhereNode(connector=expected_connector, negated=q_object.negated)
    
    assert result == expected_clause