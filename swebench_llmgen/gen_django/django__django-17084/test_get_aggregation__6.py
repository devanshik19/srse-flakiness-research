import pytest
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.sql.query import Query

@pytest.mark.parametrize("aggregate_exprs, expected", [
    ({'user_count': Count('id')}, {'user_count': 0}),
    ({'user_count': Count('id')}, {'user_count': 1}),
])
def test_get_aggregation(aggregate_exprs, expected):
    # Arrange: Create a user instance in the database
    User.objects.create(username='testuser')

    # Create query instance for the User model
    query = Query(User)

    # Act: Get aggregation results
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)

    # Assert: Check if results match the expected values
    assert result == expected

    # Clean up the created user instance
    User.objects.get(username='testuser').delete()