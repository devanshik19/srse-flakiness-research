import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_split_exclude():
    user_model = User
    query = Query(user_model)

    # Mock filter expressions for testing
    filter_exprs = [
        ('username', 'testuser'),                    # Normal case
        ('first_name', 'John'),                      # Another normal case
        ('email', OuterRef('email')),                # Using OuterRef
        ('last_name', F('last_name')),               # Using F expression
    ]
    
    for filter_expr in filter_exprs:
        can_reuse = {query.get_initial_alias()}
        names_with_path = ['user']
        
        condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)
        
        # Assertions to check if condition is not None
        assert condition is not None
        assert isinstance(condition, query.where.__class__)
        
        # Additionally check if needed_inner is of proper type or expected value
        assert isinstance(needed_inner, bool)

    # Test for checking nullable handling
    user_instance = User(username='testuser', first_name='John', last_name='Doe', email='john@example.com')
    user_instance.save()

    filter_expr_nullable = ('email', None)  # Test for nullable field
    can_reuse = {query.get_initial_alias()}
    names_with_path = ['user']

    condition, needed_inner = query.split_exclude(filter_expr_nullable, can_reuse, names_with_path)

    assert condition is not None
    assert isinstance(condition, query.where.__class__)
    assert isinstance(needed_inner, bool)