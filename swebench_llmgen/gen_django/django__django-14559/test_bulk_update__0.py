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
from django.db.models import AutoField, DateField, DateTimeField, F, Value, When, Case, Cast
from django.contrib.auth.models import User
import pytest

@pytest.mark.django_db
def test_bulk_update():
    # Create test users
    user1 = User.objects.create(username='user1', email='user1@example.com', first_name='First', last_name='User')
    user2 = User.objects.create(username='user2', email='user2@example.com', first_name='Second', last_name='User')
    objs = [user1, user2]

    # Test fields to update
    fields = ['email', 'first_name']

    # Perform bulk update
    new_email = 'updated_email@example.com'
    new_first_name = 'UpdatedName'
    for obj in objs:
        obj.email = new_email
        obj.first_name = new_first_name

    # Call the bulk_update method
    User.objects.bulk_update(objs, fields)

    # Retrieve updated users
    user1.refresh_from_db()
    user2.refresh_from_db()

    # Assertions to check if bulk update worked correctly
    assert user1.email == new_email
    assert user1.first_name == new_first_name
    assert user2.email == new_email
    assert user2.first_name == new_first_name

def test_bulk_update_empty_fields():
    user = User.objects.create(username='user3', email='user3@example.com')
    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update([user], [])

def test_bulk_update_no_primary_key():
    user = User(username='user4', email='user4@example.com')
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user], ['email'])

def test_bulk_update_with_non_concrete_field():
    user = User.objects.create(username='user5', email='user5@example.com')
    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        User.objects.bulk_update([user], ['is_superuser'])  # is_superuser is not a generic field

def test_bulk_update_with_primary_key_field():
    user = User.objects.create(username='user6', email='user6@example.com')
    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update([user], ['id'])  # 'id' is the primary key field