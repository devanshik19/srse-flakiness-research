import copy
from django.db.models import Count, Sum
from django.db.models.sql.query import Query
from django.contrib.auth.models import User

def test_get_aggregation_with_no_aggregate_exprs():
    query = Query(User)
    result = query.get_aggregation(using='default', aggregate_exprs={})
    assert result == {}

def test_get_aggregation_with_valid_aggregate_exprs():
    query = Query(User)
    aggregate_exprs = {
        'user_count': Count('id'),
        'username_length_sum': Sum('username')
    }
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    assert 'user_count' in result
    assert 'username_length_sum' in result

def test_get_aggregation_with_invalid_aggregate_expr():
    query = Query(User)
    aggregate_exprs = {
        'average_age': Count('age')  # Assuming 'age' does not exist on User model, will raise TypeError
    }
    try:
        query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    except TypeError as e:
        assert str(e) == "average_age is not an aggregate expression"

def test_get_aggregation_with_group_by():
    query = Query(User)
    query.group_by = ('username',)  # Setting a mock group_by
    aggregate_exprs = {
        'user_count': Count('id')
    }
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    assert 'user_count' in result

def test_get_aggregation_with_sliced_query():
    query = Query(User)
    query.is_sliced = True  # Mock slice
    aggregate_exprs = {
        'user_count': Count('id')
    }
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    assert 'user_count' in result