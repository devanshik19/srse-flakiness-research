import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models.sql.constants import CURSOR, GET_ITERATOR_CHUNK_SIZE, NO_RESULTS
from django.db.models.sql.query import Query
from django.db.models.sql.subqueries import UpdateQuery

@pytest.fixture
def update_query():
    uq = UpdateQuery()
    uq.related_updates = {}
    return uq

def test_get_related_updates_empty(update_query):
    assert update_query.get_related_updates() == []

def test_get_related_updates_with_no_related_ids(update_query):
    update_query.related_updates = {
        User: {'username': 'new_username'},
    }
    related_updates = update_query.get_related_updates()
    assert len(related_updates) == 1
    assert related_updates[0].values == {'username': 'new_username'}
    assert update_query.related_ids is None

def test_get_related_updates_with_related_ids(update_query):
    update_query.related_updates = {
        User: {'username': 'new_username'},
    }
    update_query.related_ids = [1, 2, 3]  # Assuming these IDs exist
    related_updates = update_query.get_related_updates()
    assert len(related_updates) == 1
    assert related_updates[0].values == {'username': 'new_username'}
    assert related_updates[0].related_ids == [1, 2, 3]
    
def test_get_related_updates_multiple_models(update_query):
    update_query.related_updates = {
        User: {'username': 'new_username'},
        User: {'email': 'new_email@example.com'},
    }
    related_updates = update_query.get_related_updates()
    assert len(related_updates) == 2
    assert related_updates[0].values == {'username': 'new_username'}
    assert related_updates[1].values == {'email': 'new_email@example.com'}