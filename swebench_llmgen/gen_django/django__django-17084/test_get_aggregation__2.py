import pytest
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_queryset():
    return User.objects.create(username='testuser', password='password123')

def test_get_aggregation_with_valid_expression(user_queryset):
    query = Query(User)
    aggregate_exprs = {
        'total_users': Sum('id'),
    }
    
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    
    assert 'total_users' in result
    assert result['total_users'] == 1  # There is one user created.

def test_get_aggregation_with_no_expressions():
    query = Query(User)
    aggregate_exprs = {}
    
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    
    assert result == {}

def test_get_aggregation_with_invalid_expression():
    query = Query(User)
    aggregate_exprs = {
        'invalid_aggregate': 'non_existent_field',
    }
    
    with pytest.raises(TypeError, match="invalid_aggregate is not an aggregate expression"):
        query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)

def test_get_aggregation_with_existing_aggregations(user_queryset):
    query = Query(User)
    query.annotations = {
        'previous_aggregation': Sum('id')
    }
    
    aggregate_exprs = {
        'new_total': Sum('id'),
    }
    
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    
    assert 'new_total' in result
    assert result['new_total'] == 1  # Verify the calculation considers existing