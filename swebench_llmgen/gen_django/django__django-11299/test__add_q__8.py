import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode

@pytest.fixture
def query_instance():
    # Create a dummy Query instance
    model = User
    where = WhereNode()
    return Query(model, where)

def test_add_q_with_simple_q(query_instance):
    q_object = Q(username='testuser')
    used_aliases = set()
    result_clause, needed_inner = query_instance._add_q(q_object, used_aliases)

    assert isinstance(result_clause, WhereNode)
    assert 'username' in str(result_clause)
    assert needed_inner is False

def test_add_q_with_negated_q(query_instance):
    q_object = Q(username='testuser', negated=True)
    used_aliases = set()
    result_clause, needed_inner = query_instance._add_q(q_object, used_aliases)

    assert isinstance(result_clause, WhereNode)
    assert 'username' in str(result_clause)
    assert needed_inner is False

def test_add_q_with_combined_q(query_instance):
    q_object = Q(username='testuser') & Q(email='test@example.com')
    used_aliases = set()
    result_clause, needed_inner = query_instance._add_q(q_object, used_aliases)

    assert isinstance(result_clause, WhereNode)
    assert 'username' in str(result_clause)
    assert 'email' in str(result_clause)
    assert needed_inner is False

def test_add_q_with_children_q(query_instance):
    q_object = Q(username='testuser') | Q(Q(email='test@example.com'))
    used_aliases = set()
    result_clause, needed_inner = query_instance._add_q(q_object, used_aliases)

    assert isinstance(result_clause, WhereNode)
    assert 'username' in str(result_clause)
    assert 'email' in str(result_clause)
    assert needed_inner is False

def test_add_q_with_no_children_q(query_instance):
    q_object = Q()
    used_aliases = set()
    result_clause, needed_inner = query_instance._add_q(q_object, used_aliases)

    assert isinstance(result_clause, WhereNode)
    assert not str(result_clause)  # It should not add any clauses
    assert needed_inner is False