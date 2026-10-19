import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def setup_query():
    # Setup a basic query with User model
    query = Query(User)
    return query

def test_add_q_with_children(setup_query):
    query = setup_query
    q_object = Q(username='testuser') & Q(is_staff=True)

    # Execute _add_q, which is private, thus we rely on public method
    target_clause, needed_inner = query._add_q(q_object, used_aliases=set())
    
    assert target_clause is not None
    assert 'username' in str(target_clause)
    assert 'is_staff' in str(target_clause)

def test_add_q_with_negation(setup_query):
    query = setup_query
    q_object = Q(username='testuser').negate()

    target_clause, needed_inner = query._add_q(q_object, used_aliases=set())
    
    assert target_clause is not None
    assert 'NOT (' in str(target_clause)

def test_add_q_with_nested_queries(setup_query):
    query = setup_query
    q_object = Q(username='testuser') | Q(Q(username='admin') & Q(is_active=True))

    target_clause, needed_inner = query._add_q(q_object, used_aliases=set())

    assert target_clause is not None
    assert 'username' in str(target_clause)
    assert 'admin' in str(target_clause)
    assert 'is_active' in str(target_clause)

def test_add_q_empty_query(setup_query):
    query = setup_query
    q_object = Q()  # Empty Q object

    target_clause, needed_inner = query._add_q(q_object, used_aliases=set())

    assert target_clause is not None
    assert target_clause.connector == 'AND'  # Should be an AND connector by default