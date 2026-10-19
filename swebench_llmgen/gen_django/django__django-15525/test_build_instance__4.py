import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.deprecation import RemovedInDjango50Warning
from django.core.serializers.base import build_instance


def test_build_instance_with_valid_data():
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'secret'
    }
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.username == 'testuser'
    assert user_instance.email == 'testuser@example.com'


def test_build_instance_with_natural_key():
    User.objects.create_user(username='testuser2', email='testuser2@example.com', password='secret')
    
    user_data = {
        'username': 'testuser2', 
        'email': 'testuser2@example.com', 
        'password': 'secret'
    }
    
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.pk is not None
    assert user_instance.username == 'testuser2'


def test_build_instance_with_natural_key_not_found():
    user_data = {
        'username': 'nonexistentuser', 
        'email': 'nonexistentuser@example.com', 
        'password': 'secret'
    }
    
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.pk is None
    assert user_instance.username == 'nonexistentuser'


def test_build_instance_without_primary_key():
    user_data = {
        'email': 'no_pk@example.com', 
        'password': 'secret'
    }
    
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.username is None
    assert user_instance.email == 'no_pk@example.com'


def test_build_instance_should_not_warn_when_pk_exists():
    with warnings.catch_warnings(record=True) as w:
        user_data = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password': 'secret'
        }
        user_instance = build_instance(User, user_data, 'default')
        assert not w  # No warnings expected