import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

def test_split_exclude_with_existing_relation():
    user = User.objects.create(username='testuser', email='test@example.com')
    user_id = user.pk

    # Create a Query object for User model
    query = Query(User)
    filter_expr = ('id', user_id)
    can_reuse = set()  # No reusable joins for this test
    names_with_path = []

    # Check the output of the split_exclude method
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)
    
    assert condition is not None  # Ensure that a condition is created
    assert isinstance(condition, Q)  # Ensure the condition is a Q object

def test_split_exclude_with_nullable_field():
    # Create a User instance
    user = User.objects.create(username='nullableuser', email='nullable@example.com', first_name=None)
    
    # Create a Query object
    query = Query(User)
    filter_expr = ('first_name', None)  # Check against nullable field
    can_reuse = set()  # No reusable joins for this test
    names_with_path = []

    # Test the split_exclude method
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)
    
    assert condition is not None  # Ensure that a condition is created
    assert isinstance(condition, Q)  # Ensure the condition is a Q object
    assert 'first_name__isnull' in str(condition)  # Ensure ISNULL check is present

def test_split_exclude_with_F_object():
    # Create a User instance
    user = User.objects.create(username='fuser', email='fuser@example.com')
    
    # Create a Query object
    query = Query(User)
    filter_expr = ('username', Q(username='fuser'))  # Using a Q object
    can_reuse = set()  # No reusable joins for this test
    names_with_path = []

    # Test the split_exclude method
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)
    
    assert condition is not None  # Ensure that a condition is created
    assert isinstance(condition, Q)  # Ensure the condition is a Q object
    assert 'username' in str(condition)  # Ensure the condition references the username field