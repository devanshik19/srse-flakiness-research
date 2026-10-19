import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

def test_query_with_deferred_filter():
    # Arrange
    user = User.objects.create(username='testuser')
    qs = User.objects.defer('password')
    qs._deferred_filter = (False, (user.username,), {})  # Setting a deferred filter

    # Act
    result_query = qs.query()

    # Assert
    assert result_query is not None
    assert qs._deferred_filter is None  # Check that _deferred_filter has been cleared
    assert 'password' not in result_query.annotations  # Ensure 'password' is deferred 

def test_query_without_deferred_filter():
    # Arrange
    qs = User.objects.all()
    # Ensure no deferred filter set
    qs._deferred_filter = None

    # Act
    result_query = qs.query()

    # Assert
    assert result_query is not None
    assert qs._deferred_filter is None  # Ensure _deferred_filter remains None