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
from django.db.models import User, F, Value, When, Case, Cast
import pytest

class TestQuerySetBulkUpdate:

    @pytest.fixture
    def user_data(self):
        return [User(username=f'user{i}', email=f'user{i}@example.com') for i in range(3)]

    @pytest.fixture
    def create_users(self, user_data):
        User.objects.bulk_create(user_data)
        return User.objects.all()

    def test_bulk_update_success(self, create_users):
        users = list(create_users)
        for user in users:
            user.email = f'updated_{user.email}'
        User.objects.bulk_update(users, ['email'])

        updated_users = User.objects.all()
        assert all(user.email.startswith('updated_') for user in updated_users)

    def test_bulk_update_empty_fields(self, create_users):
        users = list(create_users)
        with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
            User.objects.bulk_update(users, [])

    def test_bulk_update_negative_batch_size(self, create_users):
        users = list(create_users)
        with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
            User.objects.bulk_update(users, ['email'], batch_size=-1)

    def test_bulk_update_missing_primary_key(self):
        user = User(username='no_pk')
        with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
            User.objects.bulk_update([user], ['email'])

    def test_bulk_update_concrete_fields_only(self, create_users):
        users = list(create_users)
        # Attempting to update a field that isn't concrete (assuming is_staff is not concrete)
        with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
            User.objects.bulk_update(users, ['is_staff'])

    def test_bulk_update_primary_key_field(self, create_users):
        users = list(create_users)
        with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
            User.objects.bulk_update(users, ['id'])

    def test_bulk_update_no_objects(self):
        # Attempting to bulk_update with no objects should pass silently
        User.objects.bulk_update([], ['email'])