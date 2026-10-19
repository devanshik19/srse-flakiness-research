import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    # Create a query with a User model to test against
    return Query(User)

def test_resolve_expression(user_query):
    q_instance = Q(username='testuser')

    # First call to resolve_expression with default parameters
    clause = q_instance.resolve_expression(query=user_query)
    
    assert clause is not None  # Expecting a valid clause
    assert isinstance(clause, Q)  # Make sure the clause is of type Q

    # Test with allow_joins set to False
    clause_no_joins = q_instance.resolve_expression(query=user_query, allow_joins=False)
    assert clause_no_joins is not None
    assert isinstance(clause_no_joins, Q)

    # Testing with different reuse values
    reuse_clause = q_instance.resolve_expression(query=user_query, reuse=clause)
    assert reuse_clause is not None
    assert reuse_clause == clause  # Ensure it reuses the original clause

    # Test with summarize and for_save parameters
    summarize_clause = q_instance.resolve_expression(query=user_query, summarize=True, for_save=True)
    assert summarize_clause is not None
    assert isinstance(summarize_clause, Q)