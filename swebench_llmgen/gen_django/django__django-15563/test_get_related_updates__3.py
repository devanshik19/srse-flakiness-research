import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models.sql.constants import CURSOR, GET_ITERATOR_CHUNK_SIZE, NO_RESULTS
from django.db.models.sql.query import Query
from django.db.models.sql.subqueries import UpdateQuery


@pytest.fixture
def update_query():
    query = UpdateQuery()
    query.related_updates = {
        User: {'username': 'new_username'}
    }
    query.related_ids = [1, 2]
    return query


def test_get_related_updates_empty_related_updates():
    query = UpdateQuery()
    query.related_updates = {}
    assert query.get_related_updates() == []


def test_get_related_updates_with_related_updates(update_query):
    result = update_query.get_related_updates()
    assert len(result) == 1
    assert isinstance(result[0], UpdateQuery)
    assert result[0].values == {'username': 'new_username'}
    assert result[0].related_ids == [1, 2]


def test_get_related_updates_without_related_ids(update_query):
    update_query.related_ids = None
    result = update_query.get_related_updates()
    assert len(result) == 1
    assert isinstance(result[0], UpdateQuery)
    assert result[0].values == {'username': 'new_username'}
    assert result[0].related_ids is None