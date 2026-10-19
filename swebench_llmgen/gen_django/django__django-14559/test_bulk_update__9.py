import copy
import operator
import warnings
from itertools import chain
import django
from django.conf import settings
from django.core import exceptions
from django.db import IntegrityError, NotSupportedError, connections, router, transaction
from django.db.models import F, Value, Case, When, Cast
from django.contrib.auth.models import User
import pytest

class TestQuerySet:
    
    def test_bulk_update_valid(self):
        user1 = User.objects.create(username='user1', email='user1@example.com')
        user2 = User.objects.create(username='user2', email='user2@example.com')
        users = [user1, user2]
        
        # Update email addresses
        users[0].email = 'new_email1@example.com'
        users[1].email = 'new_email2@example.com'

        User.objects.bulk_update(users, ['email'])

        # Refresh objects and assert changes
        user1.refresh_from_db()
        user2.refresh_from_db()
        assert user1.email == 'new_email1@example.com'
        assert user2.email == 'new_email2@example.com'

    def test_bulk_update_empty_fields(self):
        user = User.objects.create(username='user1', email='user1@example.com')
        with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
            User.objects.bulk_update([user], [])

    def test_bulk_update_none_primary_key(self):
        user = User(username='user1', email='user1@example.com')
        with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
            User.objects.bulk_update([user], ['email'])

    def test_bulk_update_invalid_field(self):
        user = User.objects.create(username='user1', email='user1@example.com')
        with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
            User.objects.bulk_update([user], ['groups'])

    def test_bulk_update_primary_key_field(self):
        user = User.objects.create(username='user1', email='user1@example.com')
        with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
            User.objects.bulk_update([user], ['id'])

    def test_bulk_update_negative_batch_size(self):
        user = User.objects.create(username='user1', email='user1@example.com')
        with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
            User.objects.bulk_update([user], ['email'], batch_size=-1)

    def test_bulk_update_no_objects(self):
        result = User.objects.bulk_update([], ['email'])
        assert result is None  # expecting no error and no operation