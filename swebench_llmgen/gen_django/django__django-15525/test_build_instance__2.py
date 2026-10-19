import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.deprecation import RemovedInDjango50Warning
from django.core.serializers.base import build_instance

def test_build_instance_with_pk():
    user_data = {'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com'}
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.username == 'testuser'
    assert user_instance.email == 'test@example.com'
    # Note: Password is not returned as plain text for security reasons.

def test_build_instance_without_pk_and_natural_key_exists():
    # Create a user first to ensure the natural key retrieval will succeed.
    existing_user = User.objects.create(username='existinguser', password='password', email='existing@example.com')
    
    user_data = {'username': 'existinguser'}
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.pk == existing_user.pk

def test_build_instance_without_pk_and_natural_key_not_found():
    user_data = {'username': 'nonexistentuser'}
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.pk is None
    assert user_instance.username == 'nonexistentuser'

def test_build_instance_with_empty_data():
    user_data = {}
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.username == ''
    assert user_instance.email == ''