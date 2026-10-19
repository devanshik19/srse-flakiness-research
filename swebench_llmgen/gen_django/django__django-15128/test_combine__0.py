import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.constants import INNER, OR, AND

@pytest.mark.parametrize("connector, expect_exception", [
    (AND, None),  # Valid case
    (OR, None),   # Valid case
    (AND, TypeError),  # Different models case
    (OR, TypeError),   # Sliced query case
])
def test_combine(connector, expect_exception):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    query1 = Query(User)
    query2 = Query(User)
    
    query1 = query1.filter(username='user1')
    query2 = query2.filter(username='user2')

    if connector == AND:
        # Test combining two queries with AND
        result_query = query1.combine(query2, connector)
        assert result_query.where

    elif connector == OR:
        # Test combining two queries with OR
        result_query = query1.combine(query2, connector)
        assert result_query.where

    # Check exception cases
    if expect_exception is not None:
        if expect_exception == TypeError:
            with pytest.raises(TypeError):
                query1.combine(Query(User.objects.exclude(username='nonexistent')), connector)
        else:
            pytest.fail("Unexpected exception type.")
    
def test_combine_distinct_fields():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    query1 = Query(User)
    query2 = Query(User)

    query1.distinct_fields = ['username']
    query2.distinct_fields = ['email']  # Different distinct fields

    with pytest.raises(TypeError):
        query1.combine(query2, AND)

def test_combine_sliced_queries():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    query1 = Query(User)
    query2 = Query(User)

    query1 = query1.filter(username='user1')
    query2 = query2.filter(username='user2')
    
    # Slicing the first query
    query1.is_sliced = True

    with pytest.raises(TypeError):
        query1.combine(query2, AND)

    # Resetting the slice
    query1.is_sliced = False
    result_query = query1.combine(query2, AND)
    assert result_query.where