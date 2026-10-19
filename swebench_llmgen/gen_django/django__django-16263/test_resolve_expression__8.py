import pytest
from django.contrib.auth.models import User
from django.db.models import Q as DjangoQ
from django.db.models.sql import Query
from django.db.models.sql.query import QuerySet

@pytest.fixture
def user_queryset():
    # Create sample users for testing
    User.objects.create(username='user1')
    User.objects.create(username='user2')
    return User.objects.all()

def test_resolve_expression(user_queryset):
    # Instantiate the Query object
    query = Query(User)

    # Create an instance of the Q class
    q_instance = DjangoQ(username='user1')  # Using Django's Q class for compatibility
    
    # Call resolve_expression
    clause = q_instance.resolve_expression(query=query, allow_joins=True)

    # Test the clause returned
    assert isinstance(clause, QuerySet), "Expected a QuerySet clause."
    assert clause.query.where.children[0].lhs, "Left-hand side should not be None."
    assert clause.query.where.children[0].rhs == 'user1', "Right-hand side should match 'user1'."

    # Test if joins are promoted (with joins we expect at least 1)
    joins = query.get_initial_alias()
    assert query.alias_map[joins][1] == 'LEFT OUTER JOIN', "Expected left outer join."

    # Test when `allow_joins` is False
    q_instance_no_joins = DjangoQ(username='user1')

    # Create a new Query object for testing without joins
    query_no_joins = Query(User)
    clause_no_joins = q_instance_no_joins.resolve_expression(query=query_no_joins, allow_joins=False)

    # Expect the clause without any joins
    assert isinstance(clause_no_joins, QuerySet), "Expected a QuerySet clause without joins."
    
    # Verify no joins in alias_map
    assert not query_no_joins.alias_map, "No joins should be present when allow_joins is False."