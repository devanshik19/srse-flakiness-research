import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.where import WhereNode
from django.db.models.sql.query import Query

@pytest.fixture
def user():
    return User.objects.create(username='testuser', password='password')

def test_add_q_with_simple_condition(user):
    query = Query(model=User, alias_cols=False)
    q_object = Q(username='testuser')
    used_aliases = []

    target_clause, needed_inner = query._add_q(
        q_object=q_object,
        used_aliases=used_aliases
    )

    assert isinstance(target_clause, WhereNode)
    assert len(target_clause.children) == 1
    assert target_clause.children[0].lhs.name == 'username'
    assert target_clause.children[0].rhs == 'testuser'

def test_add_q_with_negation(user):
    query = Query(model=User, alias_cols=False)
    q_object = Q(username='testuser', negated=True)
    used_aliases = []

    target_clause, needed_inner = query._add_q(
        q_object=q_object,
        used_aliases=used_aliases
    )

    assert isinstance(target_clause, WhereNode)
    assert target_clause.negated
    assert len(target_clause.children) == 1
    assert target_clause.children[0].lhs.name == 'username'
    assert target_clause.children[0].rhs == 'testuser'

def test_add_q_with_multiple_conditions(user):
    query = Query(model=User, alias_cols=False)
    q_object = Q(username='testuser') & Q(password='password')
    used_aliases = []

    target_clause, needed_inner = query._add_q(
        q_object=q_object,
        used_aliases=used_aliases
    )

    assert isinstance(target_clause, WhereNode)
    assert len(target_clause.children) == 2

def test_add_q_with_branch_negated(user):
    query = Query(model=User, alias_cols=False)
    q_object = Q(username='testuser')
    used_aliases = []
    branch_negated = True

    target_clause, needed_inner = query._add_q(
        q_object=q_object,
        used_aliases=used_aliases,
        branch_negated=branch_negated
    )

    assert isinstance(target_clause, WhereNode)
    assert target_clause.negated

def test_add_q_with_allow_joins(user):
    query = Query(model=User, alias_cols=False)
    q_object = Q(username='testuser')
    used_aliases = []
    allow_joins = False

    target_clause, needed_inner = query._add_q(
        q_object=q_object,
        used_aliases=used_aliases,
        allow_joins=allow_joins
    )

    assert isinstance(target_clause, WhereNode)
    assert len(target_clause.children) == 1