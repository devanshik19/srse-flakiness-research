import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.deprecation import RemovedInDjango50Warning
from django.core.serializers.base import build_instance

@pytest.mark.django_db
def test_build_instance_with_primary_key():
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password'
    }
    user = User.objects.create(**user_data)
    user_data[User._meta.pk.attname] = user.pk

    instance = build_instance(User, user_data, 'default')

    assert instance.pk == user.pk
    assert instance.username == user.username
    assert instance.email == user.email


@pytest.mark.django_db
def test_build_instance_without_primary_key_and_natural_key():
    user_data = {
        'username': 'uniqueuser',
        'email': 'uniqueuser@example.com',
        'password': 'password'
    }
    user = User.objects.create(**user_data)
    natural_key = (user.username,)  # Username is used as a natural key

    # Simulating absence of primary key
    user_data[User._meta.pk.attname] = None

    # Add get_by_natural_key to the UserManager
    User.objects.get_by_natural_key = lambda username: User.objects.get(username=username)

    instance = build_instance(User, user_data, 'default')

    assert instance.pk == user.pk
    assert instance.username == user.username
    assert instance.email == user.email


@pytest.mark.django_db
def test_build_instance_without_primary_key_and_no_natural_key():
    user_data = {
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'password': 'password'
    }
    
    # Simulating absence of primary key and no natural key available
    user_data[User._meta.pk.attname] = None
    
    instance = build_instance(User, user_data, 'default')

    assert instance.pk is None
    assert instance.username == user_data['username']
    assert instance.email == user_data['email']


@pytest.mark.django_db
def test_build_instance_with_non_existing_natural_key():
    user_data = {
        'username': 'nonexistentuser',
        'email': 'nonexistentuser@example.com',
        'password': 'password'
    }

    # Simulating absence of primary key
    user_data[User._meta.pk.attname] = None
    
    # Override the manager method to raise ObjectDoesNotExist
    User.objects.get_by_natural_key = lambda username: (_ for _ in ()).throw(ObjectDoesNotExist)

    instance = build_instance(User, user_data, 'default')

    assert instance.pk is None
    assert instance.username == user_data['username']
    assert instance.email == user_data['email']