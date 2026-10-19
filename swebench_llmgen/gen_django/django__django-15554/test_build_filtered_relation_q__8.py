import pytest
from django.db.models.sql.where import WhereNode
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def setup_query():
    # Setup a Query instance with User model
    model = User
    query = Query(model=model, alias_cols=None)
    return query

def test_build_filtered_relation_q_with_single_condition(setup_query):
    q_object = Q(username='testuser')
    query = setup_query
    result = query.build_filtered_relation_q(q_object, reuse=False)

    assert isinstance(result, WhereNode)
    assert len(result.children) == 1
    assert result.children[0].children[0] == 'username'
    assert result.children[0].children[1] == 'testuser'

def test_build_filtered_relation_q_with_multiple_conditions(setup_query):
    q_object = Q(username='testuser') & Q(email='test@example.com')
    query = setup_query
    result = query.build_filtered_relation_q(q_object, reuse=False)

    assert isinstance(result, WhereNode)
    assert len(result.children) == 1
    assert len(result.children[0].children) == 2

def test_build_filtered_relation_q_negated_condition(setup_query):
    q_object = Q(username='testuser', negated=True)
    query = setup_query
    result = query.build_filtered_relation_q(q_object, reuse=False)

    assert isinstance(result, WhereNode)
    assert result.negated is True
    assert len(result.children) == 1

def test_build_filtered_relation_q_nested_conditions(setup_query):
    q_object = Q(username='testuser') | Q(email='test@example.com')
    query = setup_query
    result = query.build_filtered_relation_q(q_object, reuse=False)

    assert isinstance(result, WhereNode)
    assert len(result.children) == 1
    assert result.children[0].connector == 'OR'  # Check if connector is OR

def test_build_filtered_relation_q_with_branch_negation(setup_query):
    child_q = Q(username='testuser')
    parent_q = Q(child_q, negated=True)
    query = setup_query
    result = query.build_filtered_relation_q(parent_q, reuse=False)

    assert isinstance(result, WhereNode)
    assert result.negated is True
    assert len(result.children) == 1

def test_build_filtered_relation_q_empty_case(setup_query):
    q_object = Q()
    query = setup_query
    result = query.build_filtered_relation_q(q_object, reuse=False)

    assert isinstance(result, WhereNode)
    assert len(result.children) == 0