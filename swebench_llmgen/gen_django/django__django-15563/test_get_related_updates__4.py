import pytest
from django.contrib.auth.models import User
from django.db.models.sql.constants import CURSOR, GET_ITERATOR_CHUNK_SIZE, NO_RESULTS
from django.core.exceptions import FieldError
from django.db.models.sql.query import Query
from django.db.models.sql.subqueries import UpdateQuery

@pytest.mark.parametrize("related_ids, expected_count", [
    (None, 0),
    ([1, 2, 3], 2),
])
def test_get_related_updates(related_ids, expected_count):
    # Setup
    user_model = User
    user1 = user_model.objects.create_user(username='user1', password='password')
    user2 = user_model.objects.create_user(username='user2', password='password')

    update_query = UpdateQuery()
    update_query.related_updates = {
        user_model: {'email': 'new_email@example.com'},
        user_model: {'is_active': True}
    }

    update_query.related_ids = related_ids if related_ids is not None else []

    # Act
    result = update_query.get_related_updates()

    # Assert
    assert len(result) == expected_count
    if expected_count > 0:
        for query in result:
            assert isinstance(query, UpdateQuery)
            assert query.values in [{'email': 'new_email@example.com'}, {'is_active': True}]
            if related_ids is not None:
                assert query.related_ids == related_ids