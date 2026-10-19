import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def test_build_instance_with_primary_key():
    user_data = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@example.com'
    }
    user = User(**user_data)
    user.save()
    
    # Simulate data input for building an instance
    data_with_pk = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@example.com',
        'id': user.id  # primary key present
    }

    instance = build_instance(User, data_with_pk, db='default')
    assert instance.id == user.id
    assert instance.username == user_data['username']

def test_build_instance_with_natural_key():
    user_data = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@example.com'
    }
    user = User(**user_data)
    user.save()

    # Simulate natural key data input (without primary key)
    data_without_pk = {
        'username': 'testuser',
        'email': 'test@example.com'
    }

    instance = build_instance(User, data_without_pk, db='default')
    assert instance.id == user.id
    assert instance.username == user_data['username']

def test_build_instance_natural_key_not_found():
    # Simulate data input without primary key and natural key
    data_without_pk = {
        'username': 'nonexistentuser',
        'email': 'nonexistent@example.com'
    }

    instance = build_instance(User, data_without_pk, db='default')
    assert instance.username == data_without_pk['username']
    assert instance.email == data_without_pk['email']
    assert instance.id is None  # No instance found, id should be None

def test_build_instance_with_invalid_model():
    with pytest.raises(TypeError):
        build_instance(str, {}, db='default')  # Passing an invalid model