import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

def test_build_instance_with_existing_pk():
    user_data = {'id': 1, 'username': 'testuser', 'password': 'password123'}
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.id == user_data['id']
    assert user_instance.username == user_data['username']

def test_build_instance_with_natural_key():
    user = User.objects.create(username='testuser', password='password123')
    user_data = {'username': 'testuser', 'password': 'password123'}
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.id == user.id
    assert user_instance.username == user_data['username']

def test_build_instance_with_no_pk_and_no_natural_key():
    user_data = {'username': 'newuser', 'password': 'newpassword'}
    user_instance = build_instance(User, user_data, 'default')
    assert user_instance.id is None  # No pk is set
    assert user_instance.username == user_data['username']

def test_build_instance_with_non_existent_natural_key():
    user_data = {'username': 'nonexistentuser', 'password': 'password123'}
    # Attempting to use a natural key that will not be found
    with pytest.raises(ObjectDoesNotExist):
        build_instance(User, user_data, 'default')