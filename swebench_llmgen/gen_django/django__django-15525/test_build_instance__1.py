import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

def test_build_instance_with_existing_pk():
    # Given an existing user instance
    existing_user = User.objects.create(username='testuser', password='password')
    data = {'id': existing_user.id, 'username': 'newusername', 'password': 'newpassword'}

    # When building instance with existing pk
    user_instance = build_instance(User, data, db='default')

    # Then it should return an instance with the same pk
    assert user_instance.id == existing_user.id
    assert user_instance.username == 'newusername'

def test_build_instance_with_natural_key():
    # Given an existing user instance
    existing_user = User.objects.create(username='testuser', password='password')
    data = {'username': 'testuser'}

    # Override the natural_key method to match the test case
    User.natural_key = lambda self: (self.username,)
    
    # When building instance without pk but with natural key
    user_instance = build_instance(User, data, db='default')

    # Then it should retrieve the existing user instance
    assert user_instance.id == existing_user.id
    assert user_instance.username == 'testuser'

def test_build_instance_with_non_existent_natural_key():
    data = {'username': 'nonexistentuser'}

    # Override the natural_key method to match the test case
    User.natural_key = lambda self: (self.username,)

    # When building instance with non-existent natural key
    user_instance = build_instance(User, data, db='default')

    # Then it should not raise an exception and return an instance with no pk
    assert user_instance.id is None
    assert user_instance.username == 'nonexistentuser'