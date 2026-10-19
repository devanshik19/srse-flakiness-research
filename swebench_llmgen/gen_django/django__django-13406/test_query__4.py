import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


def test_query_method_with_deferred_filter():
    user = User.objects.create(username="testuser")
    qs = User.objects.all()  # Get a QuerySet
    qs._deferred_filter = (False, ('username',), {})  # Simulate a deferred filter
    assert qs.query() == qs._query  # Check if it returns the current query

    # Ensure the deferred filter is applied
    qs._filter_or_exclude_inplace(False, ('username',), {})
    assert qs._deferred_filter is None  # It should be cleared

    
def test_query_method_without_deferred_filter():
    qs = User.objects.all()  # Get a QuerySet
    # Before applying any deferred filter
    assert qs.query() == qs._query  # Check that it returns the original query