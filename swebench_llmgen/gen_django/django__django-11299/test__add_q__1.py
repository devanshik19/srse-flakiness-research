import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    user_query_instance = Query(User)
    user_query_instance.add_filter(Q(username='testuser'))
    return user_query_instance

def test_add_q_with_node(user_query):
    q_object = Q(username='testuser') & Q(is_active=True)
    used_aliases = set()
    target_clause, needed_inner = user_query._add_q(q_object, used_aliases)
    
    assert target_clause is not None
    assert needed_inner == 0

def test_add_q_with_negation(user_query):
    q_object = Q(username='testuser') & Q(is_active=False)
    used_aliases = set()
    target_clause, needed_inner = user_query._add_q(q_object, used_aliases, branch_negated=True)
    
    assert target_clause is not None
    assert needed_inner == 0

def test_add_q_with_subquery(user_query):
    q_object = Q(username__icontains='user')
    used_aliases = set()
    target_clause, needed_inner = user_query._add_q(q_object, used_aliases, split_subq=True)
    
    assert target_clause is not None
    assert needed_inner == 0

def test_add_q_with_multiple_children(user_query):
    q_object = Q(username='testuser') | Q(email='test@example.com')
    used_aliases = set()
    target_clause, needed_inner = user_query._add_q(q_object, used_aliases, allow_joins=False)
    
    assert target_clause is not None
    assert needed_inner == 0

def test_add_q_with_simple_col(user_query):
    q_object = Q(first_name='John')
    used_aliases = set()
    target_clause, needed_inner = user_query._add_q(q_object, used_aliases, simple_col=True)
    
    assert target_clause is not None
    assert needed_inner == 0