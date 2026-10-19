import pytest
from django.contrib.auth.models import User
from django.db.models import Aggregate, Sum
from django.db.models.sql.query import Query


# Create a custom Aggregate for testing purposes
class TestAggregate(Aggregate):
    pass


@pytest.mark.parametrize(
    "aggregate_exprs, expected",
    [
        ({"total": Sum("id")}, {"total": 1}),  # Simple aggregation with one entry
        ({"total": Sum("id")}, {"total": 6}),  # Aggregate with multiple entries
        ({"total": TestAggregate("id")}, {"total": 6}),  # Testing a custom aggregate
    ],
)
def test_get_aggregation(aggregate_exprs, expected):
    # Set up test data
    User.objects.create(username="user1")
    User.objects.create(username="user2")
    User.objects.create(username="user3")

    # Create a Query instance
    user_query = Query(model=User)

    # Check the aggregation results
    result = user_query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    assert result == expected


def test_get_aggregation_no_aggregates():
    user_query = Query(model=User)
    result = user_query.get_aggregation(using='default', aggregate_exprs={})
    assert result == {}