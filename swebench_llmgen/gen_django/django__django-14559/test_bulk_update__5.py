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
from django.db.models import AutoField, Value, When, Case, F, Cast
from django.contrib.auth.models import User
import pytest

@pytest.mark.django_db
def test_bulk_update():
    # Prepare test data
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    users = [user1, user2]
    
    # Update fields to modify
    fields = ['email']

    # Test successful bulk update
    User.objects.bulk_update(users, fields)
    assert User.objects.get(pk=user1.pk).email == 'user1@example.com'
    assert User.objects.get(pk=user2.pk).email == 'user2@example.com'

    # Update the users' email addresses
    user1.email = 'new_user1@example.com'
    user2.email = 'new_user2@example.com'

    # Test bulk update with modified objects
    User.objects.bulk_update(users, fields)
    assert User.objects.get(pk=user1.pk).email == 'new_user1@example.com'
    assert User.objects.get(pk=user2.pk).email == 'new_user2@example.com'

    # Test bulk update with empty fields
    with pytest.raises(ValueError, match='Field names must be given to bulk_update()'):
        User.objects.bulk_update(users, [])

    # Test bulk update with negative batch size
    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        User.objects.bulk_update(users, fields, batch_size=-1)

    # Test bulk update with None primary key
    user3 = User(username='user3', email='user3@example.com')
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user3], fields)

    # Test bulk update with many-to-many field
    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        User.objects.bulk_update(users, ['groups'])

    # Test bulk update with primary key field
    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update(users, ['id'])