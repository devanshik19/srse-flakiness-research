import pytest
from django.contrib.auth.models import User
from django.db.models import Q as DjangoQ
from django.db.models.sql.query import Query

@pytest.fixture
def user_queryset(db):
    return User.objects.all()

def test_resolve_expression(user_queryset):
    q_instance = DjangoQ(username='testuser')

    # Simulate a Query object which is normally passed in from the ORM
    query = Query(User)
    clause = q_instance.resolve_expression(query=query, allow_joins=True)

    # Assert that the resulting clause is a valid SQL expression
    assert clause is not None
    assert hasattr(clause, 'children')

    # We should also check if the query's joins have been promoted correctly
    assert query.joins
    assert all(join.join_type == 'LEFT OUTER JOIN' for join in query.joins)

    # Test the behavior with summarize flag set to True
    clause_summarized = q_instance.resolve_expression(query=query, summarize=True)
    assert clause_summarized is not None
    assert hasattr(clause_summarized, 'children')

    # Assert that summarize doesn't affect the join promotion
    assert query.joins
    assert all(join.join_type == 'LEFT OUTER JOIN' for join in query.joins)

    # Test the behavior when allow_joins is False
    clause_no_joins = q_instance.resolve_expression(query=query, allow_joins=False)
    assert clause_no_joins is not None
    assert hasattr(clause_no_joins, 'children')
    assert not query.joins  # No joins should be added