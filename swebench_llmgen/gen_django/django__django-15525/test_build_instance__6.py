import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.deprecation import RemovedInDjango50Warning

def test_build_instance_with_primary_key():
    user_data = {'username': 'testuser', 'password': 'testpass'}
    user = User(**user_data)
    user.save()

    data = {'id': user.id, 'username': 'testuser'}
    instance = build_instance(User, data, 'default')
    assert instance.id == user.id
    assert instance.username == user.username

def test_build_instance_without_primary_key_and_natural_key():
    user_data = {'username': 'testuser2', 'password': 'testpass2'}
    user = User(**user_data)
    user.save()

    data = {'username': 'testuser2'}
    instance = build_instance(User, data, 'default')
    assert instance.id == user.id
    assert instance.username == user.username

def test_build_instance_without_primary_key_and_natural_key_not_found():
    data = {'username': 'nonexistentuser'}
    instance = build_instance(User, data, 'default')
    assert instance.username == 'nonexistentuser'
    assert instance.id is None

def test_build_instance_with_no_natural_key_method():
    class CustomModel:
        _meta = type('Meta', (), {'default_manager': None, 'pk': type('PK', (), {'attname': 'id', 'to_python': lambda self, x: x})()})

    data = {'id': None}
    instance = build_instance(CustomModel, data, 'default')
    assert instance.id is None