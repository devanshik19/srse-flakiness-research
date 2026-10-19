import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode

@pytest.fixture
def query_instance():
    return Query(model=None, alias_cols={})

def test_build_filtered_relation_q_with_children(query_instance):
    # Create a mock Q object with children
    q_object = Q('username__icontains', 'test')
    q_object.connector = 'AND'
    q_object.negated = False
    query_instance.add_q(q_object)

    result = query_instance.build_filtered_relation_q(q_object, reuse=None)

    # Validate the result is a WhereNode with correct properties
    assert isinstance(result, WhereNode)
    assert result.connector == 'AND'
    assert result.negated is False
    assert len(result.children) == 1

def test_build_filtered_relation_q_with_negated(query_instance):
    # Create a mock Q object with negation
    q_object = Q('username__icontains', 'test', negated=True)
    q_object.connector = 'OR'
    query_instance.add_q(q_object)

    result = query_instance.build_filtered_relation_q(q_object, reuse=None)

    # Validate the result is a WhereNode with negation
    assert isinstance(result, WhereNode)
    assert result.connector == 'OR'
    assert result.negated is True
    assert len(result.children) == 1

def test_build_filtered_relation_q_with_child_nodes(query_instance):
    # Create nested Q objects as children
    child_q1 = Q('username__icontains', 'test')
    child_q2 = Q('email__icontains', 'example.com')
    parent_q = Q(child_q1) & Q(child_q2)
    parent_q.connector = 'AND'
    parent_q.negated = False

    result = query_instance.build_filtered_relation_q(parent_q, reuse=None)

    # Validate the result
    assert isinstance(result, WhereNode)
    assert len(result.children) == 2
    assert all(isinstance(child, WhereNode) for child in result.children)

def test_build_filtered_relation_q_with_mixed_negation(query_instance):
    # Create a mixed Q object structure
    q_object = Q('username__icontains', 'test') | Q('email__icontains', 'example.com', negated=True)
    q_object.connector = 'OR'
    q_object.negated = False

    result = query_instance.build_filtered_relation_q(q_object, reuse=None)

    # Validate the result
    assert isinstance(result, WhereNode)
    assert result.connector == 'OR'
    assert len(result.children) == 2
    assert result.children[1].negated is True