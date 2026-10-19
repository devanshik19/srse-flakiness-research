import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models.sql.constants import CURSOR, GET_ITERATOR_CHUNK_SIZE, NO_RESULTS
from django.db.models.sql.query import Query
from django.db.models.sql.subqueries import UpdateQuery

@pytest.fixture
def update_query_with_related_updates():
    # Create an instance of UpdateQuery with related updates
    uq = UpdateQuery()
    uq.related_updates = {
        User: {'field_name': 'value'}  # Assuming some field update
    }
    uq.related_ids = [1, 2, 3]  # Example related IDs
    return uq

@pytest.fixture
def update_query_without_related_updates():
    # Create an instance of UpdateQuery without related updates
    uq = UpdateQuery()
    uq.related_updates = {}
    return uq

def test_get_related_updates_with_updates(update_query_with_related_updates):
    result = update_query_with_related_updates.get_related_updates()
    assert len(result) == 1
    assert isinstance(result[0], UpdateQuery)
    assert result[0].values == {'field_name': 'value'}
    assert 'pk__in' in result[0].filters  # test that the filter was added
    assert result[0].filters['pk__in'] == [1, 2, 3]

def test_get_related_updates_without_updates(update_query_without_related_updates):
    result = update_query_without_related_updates.get_related_updates()
    assert result == []