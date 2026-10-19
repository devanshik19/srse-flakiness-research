import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

def build_instance(Model, data, db):
    """
    Build a model instance.

    If the model instance doesn't have a primary key and the model supports
    natural keys, try to retrieve it from the database.
    """
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
    # Create a user with a natural key
    user = User.objects.create_user(username='testuser', password='testpass')
    natural_key_data = {
        'username': 'testuser',
    }
    
    instance = build_instance(User, natural_key_data, 'default')
    
    assert instance.pk is not None
    assert instance.username == 'testuser'

def test_build_instance_without_natural_key():
    # Providing data without natural key
    instance_data = {
        'username': 'user_without_natural_key',
        'password': 'testpass'
    }
    
    instance = build_instance(User, instance_data, 'default')
    
    assert instance.pk is None
    assert instance.username == 'user_without_natural_key'

def test_build_instance_with_invalid_natural_key():
    # Attempt to build an instance with a non-existing natural key
    natural_key_data = {
        'username': 'non_existent_user',
    }
    
    instance = build_instance(User, natural_key_data, 'default')
    
    assert instance.pk is None
    assert instance.username == 'non_existent_user'