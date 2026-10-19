import pytest
from django.contrib.auth.models import User
from django.db.models.sql.subqueries import UpdateQuery
from django.core.exceptions import FieldError

def test_get_related_updates_empty():
    query = UpdateQuery()
    query.related_updates = {}
    result = query.get_related_updates()
    assert result == []

def test_get_related_updates_no_related_ids():
    user = User.objects.create(username='testuser')
    query = UpdateQuery()
    query.related_updates = {User: {'username': 'updateduser'}}
    query.related_ids = None
    result = query.get_related_updates()
    assert len(result) == 1
    assert result[0].values == {'username': 'updateduser'}
    assert query.related_ids is None

def test_get_related_updates_with_related_ids():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    query = UpdateQuery()
    query.related_updates = {User: {'username': 'updateduser'}}
    query.related_ids = [user1.pk, user2.pk]
    result = query.get_related_updates()
    assert len(result) == 1
    assert result[0].values == {'username': 'updateduser'}
    assert hasattr(result[0], 'add_filter')

def test_get_related_updates_multiple_models():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    query = UpdateQuery()
    query.related_updates = {
        User: {'username': 'updateduser'},
        # Assume there's another model we can query
        # For testing purpose, we'll use User again with different values
        User: {'email': 'updated@example.com'}
    }
    query.related_ids = [user1.pk, user2.pk]
    result = query.get_related_updates()
    assert len(result) == 2
    assert result[0].values == {'username': 'updateduser'}
    assert result[1].values == {'email': 'updated@example.com'}