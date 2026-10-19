import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.deprecation import RemovedInDjango50Warning
from django.db import models

def test_build_instance_with_primary_key():
    user_data = {'username': 'testuser', 'password': 'password123'}
    user_instance = build_instance(User, user_data, 'default')

    assert isinstance(user_instance, User)
    assert user_instance.username == 'testuser'
    assert user_instance.pk is None  # Not saved yet

    # Save the instance to the database and verify
    user_instance.save()
    assert user_instance.pk is not None

def test_build_instance_without_primary_key_and_natural_key():
    user_data = {'username': 'naturaluser', 'password': 'password123'}
    user_instance = User.objects.create(**user_data)
    
    assert user_instance.pk is not None  # Ensure the user instance is saved
    
    # Now try building an instance without a primary key using natural key
    new_user_data = {'username': 'naturaluser'}
    new_user_instance = build_instance(User, new_user_data, 'default')

    assert isinstance(new_user_instance, User)
    assert new_user_instance.pk == user_instance.pk  # Should match the original instance's PK

def test_build_instance_without_natural_key():
    user_data = {'username': 'user_without_natural_key'}
    user_instance = build_instance(User, user_data, 'default')

    assert isinstance(user_instance, User)
    assert user_instance.username == 'user_without_natural_key'
    assert user_instance.pk is None  # Not saved yet