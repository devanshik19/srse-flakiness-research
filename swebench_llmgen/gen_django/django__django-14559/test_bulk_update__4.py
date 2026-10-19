import copy
import operator
import warnings
from itertools import chain
import django
from django.conf import settings
from django.core import exceptions
from django.db import (
    IntegrityError, NotSupportedError, connections,
    router, transaction,
)
from django.db.models import AutoField, DateField, DateTimeField
from django.db.models import Case, Value, When
from django.contrib.auth.models import User
import pytest


class TestQuerySetBulkUpdate:

    @pytest.fixture
    def user_instances(self):
        # Create User instances for testing
        user1 = User.objects.create(username='user1', email='user1@example.com')
        user2 = User.objects.create(username='user2', email='user2@example.com')
        return user1, user2

    def test_bulk_update_success(self, user_instances):
        user1, user2 = user_instances
        user1.email = 'new_email1@example.com'
        user2.email = 'new_email2@example.com'
        User.objects.bulk_update([user1, user2], ['email'])

        user1.refresh_from_db()
        user2.refresh_from_db()
        assert user1.email == 'new_email1@example.com'
        assert user2.email == 'new_email2@example.com'

    def test_bulk_update_empty_fields(self, user_instances):
        user1, user2 = user_instances
        with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
            User.objects.bulk_update([user1, user2], [])

    def test_bulk_update_no_primary_key(self):
        user = User(username='user3', email='user3@example.com')
        with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
            User.objects.bulk_update([user], ['email'])

    def test_bulk_update_with_negative_batch_size(self, user_instances):
        user1, user2 = user_instances
        with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
            User.objects.bulk_update([user1, user2], ['email'], batch_size=-1)

    def test_bulk_update_with_primary_key_field(self, user_instances):
        user1, user2 = user_instances
        with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
            User.objects.bulk_update([user1, user2], ['id'])

    def test_bulk_update_with_non_concrete_fields(self, user_instances):
        user1, user2 = user_instances
        with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
            User.objects.bulk_update([user1, user2], ['is_active'])  # Assuming is_active is a concrete field
            
    def test_bulk_update_no_objs(self):
        User.objects.bulk_update([], ['email'])  # Should not raise an error