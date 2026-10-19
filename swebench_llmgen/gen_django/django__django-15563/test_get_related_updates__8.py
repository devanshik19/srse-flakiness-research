import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models.sql.constants import CURSOR, GET_ITERATOR_CHUNK_SIZE, NO_RESULTS
from django.db.models.sql.query import Query
from django.db.models.sql.subqueries import UpdateQuery

@pytest.mark.parametrize("related_updates, related_ids, expected_count", [
    ({}, None, 0),  # No related updates
    ({User: {'field1': 'value1'}}, None, 1),  # Single update without related_ids
    ({User: {'field1': 'value1'}}, [1, 2, 3], 1),  # Single update with related_ids
])
def test_get_related_updates(related_updates, related_ids, expected_count):
    # Arrange
    update_query = UpdateQuery()
    update_query.related_updates = related_updates
    update_query.related_ids = related_ids

    # Act
    result = update_query.get_related_updates()

    # Assert
    assert len(result) == expected_count
    if expected_count > 0:
        assert isinstance(result[0], UpdateQuery)
        assert result[0].values == related_updates[User]
        if related_ids:
            assert "pk__in" in update_query.compiler.query.where.children[0].expressions[0].lhs.name