import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


def test_query_with_deferred_filter():
    # Create a User instance
    user = User.objects.create_user(username='testuser', password='testpass')

    # Create a QuerySet from User model
    qs = User.objects.all()

    # Set a deferred filter
    qs._deferred_filter = (False, ['username'], {})

    # Ensure that the query is not immediately executed
    assert qs.query() is not None

    # Check that deferred_filter is applied
    qs._filter_or_exclude_inplace(False, ['username'], {})
    assert qs.query().set['username'] == ['testuser']

    # Check the deferred_filter is reset after applying
    qs.query()
    assert qs._deferred_filter is None

def test_query_without_deferred_filter():
    # Create a QuerySet from User model
    qs = User.objects.all()

    # Ensure that there is no deferred filter
    qs._deferred_filter = None

    # Simply execute the query
    result_query = qs.query()

    # Make sure the query is the same as expected
    assert result_query is not None