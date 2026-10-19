import copy
import operator
import warnings
from itertools import chain
import django
from django.conf import settings
from django.core import exceptions
from django.db import (
    IntegrityError, NotSupportedError, connections,
    transaction,
)
from django.db.models import AutoField, User
from django.db.models.expressions import Value, When, Case
from django.db.models.functions import Cast

class TestQuerySetBulkUpdate:
    def test_bulk_update_with_valid_data(self):
        user1 = User.objects.create(username='user1', email='user1@example.com')
        user2 = User.objects.create(username='user2', email='user2@example.com')
        users = User.objects.filter(pk__in=[user1.pk, user2.pk])

        users.bulk_update([user1, user2], ['email'])

        user1.refresh_from_db()
        user2.refresh_from_db()

        assert user1.email == 'user1@example.com'
        assert user2.email == 'user2@example.com'

    def test_bulk_update_with_empty_fields(self):
        user1 = User.objects.create(username='user1', email='user1@example.com')
        users = User.objects.filter(pk=user1.pk)
        
        with pytest.raises(ValueError, match='Field names must be given to bulk_update()'):
            users.bulk_update([user1], [])

    def test_bulk_update_with_none_primary_key(self):
        user = User(username='user3', email='user3@example.com')
        
        with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
            User.objects.bulk_update([user], ['email'])

    def test_bulk_update_with_non_concrete_field(self):
        user1 = User.objects.create(username='user1', email='user1@example.com')
        users = User.objects.filter(pk=user1.pk)

        with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
            users.bulk_update([user1], ['id'])  # 'id' being the primary key field

    def test_bulk_update_with_negative_batch_size(self):
        user1 = User.objects.create(username='user1', email='user1@example.com')
        user2 = User.objects.create(username='user2', email='user2@example.com')
        users = User.objects.filter(pk__in=[user1.pk, user2.pk])

        with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
            users.bulk_update([user1, user2], ['email'], batch_size=-1)

    def test_bulk_update_with_large_batch_size(self):
        user1 = User.objects.create(username='user1', email='user1@example.com')
        user2 = User.objects.create(username='user2', email='user2@example.com')
        users = User.objects.filter(pk__in=[user1.pk, user2.pk])

        users.bulk_update([user1, user2], ['email'], batch_size=100)  # Batch size larger than the number of objects

        user1.refresh_from_db()
        user2.refresh_from_db()

        assert user1.email == 'user1@example.com'
        assert user2.email == 'user2@example.com'