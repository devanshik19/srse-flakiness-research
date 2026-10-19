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
from django.db.models import AutoField, Value, When, Case, F
from django.contrib.auth.models import User
import pytest

class QuerySetTests:

    @pytest.fixture
    def users(self):
        return [
            User.objects.create(username=f'user{i}', email=f'user{i}@example.com')
            for i in range(5)
        ]
    
    def test_bulk_update_valid(self, users):
        # Preparing the users with a known value to update
        for user in users:
            user.first_name = 'Initial'
            user.save()
        
        # Updating first names in bulk
        for i, user in enumerate(users):
            user.first_name = f'Updated{i}'
        
        User.objects.bulk_update(users, ['first_name'])

        # Verifying the updates
        for i, user in enumerate(users):
            assert User.objects.get(pk=user.pk).first_name == f'Updated{i}'

    def test_bulk_update_empty_fields(self, users):
        with pytest.raises(ValueError, match='Field names must be given to bulk_update()'):
            User.objects.bulk_update(users, [])

    def test_bulk_update_invalid_batch_size(self, users):
        with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
            User.objects.bulk_update(users, ['first_name'], batch_size=-1)

    def test_bulk_update_objects_without_pk(self):
        user = User(username='testuser', email='testuser@example.com')
        with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
            User.objects.bulk_update([user], ['first_name'])

    def test_bulk_update_non_concrete_fields(self, users):
        # Trying to update a non-concrete field (e.g. many-to-many would require a different approach)
        with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
            User.objects.bulk_update(users, ['groups'])

    def test_bulk_update_primary_key_field(self, users):
        with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
            User.objects.bulk_update(users, ['id'])