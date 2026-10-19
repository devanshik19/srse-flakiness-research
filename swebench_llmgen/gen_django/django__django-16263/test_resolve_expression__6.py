import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    # Create a user instance for testing
    User.objects.create(username='testuser', password='password')
    query = Query(User)
    return query

def test_resolve_expression(user_query):
    q_object = Q(username='testuser')
    # Ensure we have an initial state for joins
    assert not user_query.joins

    # Call the resolve_expression method
    clause = q_object.resolve_expression(query=user_query)

    # Check the clause created
    assert clause is not None
    assert not isinstance(clause, FieldError)

    # Ensure that we promoted the joins
    assert user_query.joins  # Should have joins after resolve_expression

def test_resolve_expression_no_joins(user_query):
    q_object = Q(username='non_existing_user')
    
    # Query should remain unchanged
    initial_joins_count = len(user_query.joins)

    # Call resolve_expression on a non-matching query
    clause = q_object.resolve_expression(query=user_query)

    # Check the clause created
    assert clause is not None
    assert not isinstance(clause, FieldError)
    
    # Ensure that we have not added any new joins
    assert len(user_query.joins) == initial_joins_count