import pytest
from django.db.models.sql.where import WhereNode
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    return Query(User)

def test_build_filtered_relation_q_with_simple_q(user_query):
    q_object = Q(username='testuser')
    result = user_query.build_filtered_relation_q(q_object, reuse=None)
    expected_clause = WhereNode(connector='AND', negated=False)
    expected_clause.add(user_query.build_filter('username', can_reuse=None)[0], 'AND')

    assert str(result) == str(expected_clause)

def test_build_filtered_relation_q_with_negated_q(user_query):
    q_object = Q(username='testuser', negated=True)
    result = user_query.build_filtered_relation_q(q_object, reuse=None)
    expected_clause = WhereNode(connector='AND', negated=True)
    expected_clause.add(user_query.build_filter('username', can_reuse=None)[0], 'AND')

    assert str(result) == str(expected_clause)

def test_build_filtered_relation_q_with_children_q(user_query):
    q_object = Q(username='testuser') & Q(email='test@example.com')
    result = user_query.build_filtered_relation_q(q_object, reuse=None)
    expected_clause = WhereNode(connector='AND', negated=False)
    
    for child in q_object.children:
        expected_clause.add(user_query.build_filter(child, can_reuse=None)[0], 'AND')

    assert str(result) == str(expected_clause)

def test_build_filtered_relation_q_with_nested_q(user_query):
    q_object = Q(username='testuser') | Q(Q(email='test@example.com') & Q(is_active=True))
    result = user_query.build_filtered_relation_q(q_object, reuse=None)
    expected_clause = WhereNode(connector='OR', negated=False)

    expected_clause.add(user_query.build_filter('username', can_reuse=None)[0], 'OR')

    nested_clause = WhereNode(connector='AND', negated=False)
    nested_clause.add(user_query.build_filter('email', can_reuse=None)[0], 'AND')
    nested_clause.add(user_query.build_filter('is_active', can_reuse=None)[0], 'AND')
    
    expected_clause.add(nested_clause, 'OR')

    assert str(result) == str(expected_clause)