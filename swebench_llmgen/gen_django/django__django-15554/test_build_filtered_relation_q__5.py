import pytest
from django.db.models.sql.where import WhereNode
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query_instance():
    return Query(User)

def test_build_filtered_relation_q_and(query_instance):
    q_object = Q(username='testuser') & Q(is_active=True)
    result = query_instance.build_filtered_relation_q(q_object, reuse=False)

    assert isinstance(result, WhereNode)
    assert result.connector == 'AND'
    assert not result.negated
    assert len(result.children) == 2

def test_build_filtered_relation_q_or(query_instance):
    q_object = Q(username='testuser') | Q(is_active=True)
    result = query_instance.build_filtered_relation_q(q_object, reuse=False)

    assert isinstance(result, WhereNode)
    assert result.connector == 'OR'
    assert not result.negated
    assert len(result.children) == 2

def test_build_filtered_relation_q_negated(query_instance):
    q_object = Q(username='testuser', negated=True)
    result = query_instance.build_filtered_relation_q(q_object, reuse=False, branch_negated=False)

    assert isinstance(result, WhereNode)
    assert result.negated
    assert len(result.children) == 1

def test_build_filtered_relation_q_complex(query_instance):
    q_object = Q(username='testuser') & (Q(is_active=True) | Q(is_staff=True))
    result = query_instance.build_filtered_relation_q(q_object, reuse=False)

    assert isinstance(result, WhereNode)
    assert result.connector == 'AND'
    assert not result.negated
    assert len(result.children) == 2

    child_clauses = [child for child in result.children if isinstance(child, WhereNode)]
    assert len(child_clauses) == 1  # There should be one AND clause for the username condition
    assert len(child_clauses[0].children) == 2  # Two OR conditions inside the AND clause

def test_build_filtered_relation_q_empty_children(query_instance):
    q_object = Q()
    result = query_instance.build_filtered_relation_q(q_object, reuse=False)

    assert isinstance(result, WhereNode)
    assert len(result.children) == 0