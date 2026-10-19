import pytest
from django.contrib.auth.models import User
from django.db.models import Q

def test_query_with_deferred_filter():
    user = User.objects.create_user(username='testuser', password='testpassword')
    queryset = User.objects.filter(username='testuser')
    queryset._deferred_filter = (False, [Q(username='testuser')], {})
    
    result = queryset.query()
    
    # Assert that the deferred filter is applied
    assert queryset._query.where.clauses[0].__str__() == "username = testuser"
    assert list(result) == [user]

def test_query_without_deferred_filter():
    user = User.objects.create_user(username='testuser', password='testpassword')
    queryset = User.objects.all()  # No filters applied
    
    result = queryset.query()
    
    # Assert that we can still get all users
    assert list(result) == [user]