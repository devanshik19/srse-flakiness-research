import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

def build_instance(Model, data, db):
    default_manager = Model._meta.default_manager
    pk = data.get(Model._meta.pk.attname)
    if (
        pk is None
        and hasattr(default_manager, "get_by_natural_key")
        and hasattr(Model, "natural_key")
    ):
        natural_key = Model(**data).natural_key()
        try:
            data[Model._meta.pk.attname] = Model._meta.pk.to_python(
                default_manager.db_manager(db).get_by_natural_key(*natural_key).pk
            )
        except Model.DoesNotExist:
            pass
    return Model(**data)

def test_build_instance_with_natural_key():
    # Create User instance with natural key attributes
    user = User.objects.create(username='testuser', email='test@example.com')
    natural_key_data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    
    # Try to build an instance with the natural key
    instance = build_instance(User, natural_key_data, db='default')
    
    assert instance.pk == user.pk
    assert instance.username == user.username
    assert instance.email == user.email

def test_build_instance_without_natural_key():
    data = {
        'username': 'newuser',
        'email': 'new@example.com'
    }
    
    instance = build_instance(User, data, db='default')
    
    assert instance.username == data['username']
    assert instance.email == data['email']
    assert instance.pk is None  # Ensure no pk is assigned since it doesn't exist yet

def test_build_instance_with_nonexistent_natural_key():
    data = {
        'username': 'nonexistentuser',
        'email': 'nonexistent@example.com'
    }
    
    instance = build_instance(User, data, db='default')
    
    assert instance.username == data['username']
    assert instance.email == data['email']
    assert instance.pk is None  # Ensure no pk is assigned since it doesn't exist