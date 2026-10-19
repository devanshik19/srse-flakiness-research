import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.db.models import Q

@pytest.fixture
def user_queryset():
    User.objects.create(username='user1', password='password1')
    User.objects.create(username='user2', password='password2')
    return User.objects.all()

def test_resolve_expression(user_queryset):
    # Create a Q object
    q_object = Q(username='user1')

    # Mock the query by getting the connection's query for the user queryset
    query = user_queryset._query
    
    # Test the `resolve_expression` method
    clause = q_object.resolve_expression(query=query, allow_joins=True)

    # Check the type of the returned clause (it's usually an expression)
    assert isinstance(clause, Q)

    # Check that the clause has the correct conditions
    assert clause.children == [('exact', 'user1')]