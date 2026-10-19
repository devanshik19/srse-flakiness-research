import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

def test_query_with_deferred_filter():
    # Create a user instance
    user = User.objects.create(username='testuser', password='testpassword')

    # Create a QuerySet for User model
    queryset = User.objects.all()

    # Verify that the query is initially the same as default
    initial_query = queryset.query
    assert queryset.query == initial_query

    # Set a deferred filter
    queryset._deferred_filter = (False, ('username',), {})
    
    # Call the query method to apply the deferred filter
    result_query = queryset.query()

    # Verify that the deferred filter has been applied
    assert result_query != initial_query
    assert list(queryset) == [user]  # Verify it includes the created user

    # Check that _deferred_filter is reset
    assert queryset._deferred_filter is None

def test_query_without_deferred_filter():
    # Create a user instance
    user = User.objects.create(username='anotheruser', password='anotherpassword')
    
    # Create a QuerySet for User model
    queryset = User.objects.all()

    # Initially, there should be no deferred filter
    queryset._deferred_filter = None

    # Call the query method
    result_query = queryset.query()

    # Verify that the query is unchanged without filters
    assert result_query == queryset.query

    # Verify that the queryset returns the correct user
    assert list(queryset) == [user]  # Verify it includes the created user