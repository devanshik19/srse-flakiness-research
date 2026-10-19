import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.where import WhereNode
from django.db.models.sql.query import Query

def test_add_q_simple_filter():
    query = Query(User)
    q_object = Q(username='testuser')
    used_aliases = {}

    target_clause, needed_inner = query._add_q(q_object, used_aliases)

    assert isinstance(target_clause, WhereNode)
    assert len(target_clause.children) == 1
    assert target_clause.children[0].get_sql() == "(`auth_user`.`username` = testuser)"
    assert needed_inner is True

def test_add_q_complex_filter():
    query = Query(User)
    q_object = Q(Q(username='testuser') | Q(email='user@example.com'))
    used_aliases = {}

    target_clause, needed_inner = query._add_q(q_object, used_aliases)

    assert isinstance(target_clause, WhereNode)
    assert len(target_clause.children) == 2
    assert target_clause.connector == 'OR'
    assert needed_inner is True

def test_add_q_negated_filter():
    query = Query(User)
    q_object = Q(username='testuser', negated=True)
    used_aliases = {}

    target_clause, needed_inner = query._add_q(q_object, used_aliases)

    assert isinstance(target_clause, WhereNode)
    assert len(target_clause.children) == 1
    assert target_clause.children[0].get_sql() == "(`auth_user`.`username` != testuser)"
    assert needed_inner is True

def test_add_q_with_branch_negation():
    query = Query(User)
    q_object = Q(username='testuser', negated=True)
    used_aliases = {}
    branch_negated = True

    target_clause, needed_inner = query._add_q(q_object, used_aliases, branch_negated=branch_negated)

    assert isinstance(target_clause, WhereNode)
    assert len(target_clause.children) == 1
    assert target_clause.children[0].get_sql() == "(`auth_user`.`username` != testuser)"
    assert needed_inner is True