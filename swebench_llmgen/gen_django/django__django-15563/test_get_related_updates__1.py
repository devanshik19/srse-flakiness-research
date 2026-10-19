import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models.sql.constants import CURSOR, GET_ITERATOR_CHUNK_SIZE, NO_RESULTS
from django.db.models.sql.query import Query
from django.db.models.sql.subqueries import UpdateQuery

@pytest.mark.parametrize("related_updates, related_ids, expected", [
    ({}, None, []),  # No related updates
    ({
        User: {'username': 'new_username'},
    }, None, [
        UpdateQuery(User).add_filter("pk__in", None).values={'username': 'new_username'}
    ]),  # With related updates, no related_ids
    ({
        User: {'username': 'new_username'},
    }, [1, 2, 3], [
        UpdateQuery(User).add_filter("pk__in", [1, 2, 3]).values={'username': 'new_username'}
    ]),  # With related updates and related_ids
])
def test_get_related_updates(related_updates, related_ids, expected):
    # Arrange
    query = UpdateQuery()
    query.related_updates = related_updates
    query.related_ids = related_ids

    # Act
    result = query.get_related_updates()

    # Assert
    assert len(result) == len(expected)
    for res, exp in zip(result, expected):
        assert res.values == exp.values
        assert res.related_ids == exp.related_ids if related_ids is not None else res.related_ids is None