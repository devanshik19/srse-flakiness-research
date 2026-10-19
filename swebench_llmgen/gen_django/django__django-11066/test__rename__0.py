import pytest
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.apps import apps
from django.db import connections
from django.db import transaction
from django.contrib.contenttypes.management import RenameContentType

@pytest.fixture
def rename_content_type():
    return RenameContentType(app_label='auth', old_model='user', new_model='user_new')

def test_rename_existing_content_type(rename_content_type):
    # Arrange
    old_model = 'user'
    new_model = 'user_new'
    ContentType.objects.create(app_label='auth', model=old_model)

    # Act
    rename_content_type._rename(apps, connections[DEFAULT_DB_ALIAS].schema_editor(), old_model, new_model)

    # Assert
    updated_content_type = ContentType.objects.get(app_label='auth', model=new_model)
    assert updated_content_type is not None

def test_rename_non_existing_content_type(rename_content_type):
    # Arrange
    old_model = 'non_existing_model'
    new_model = 'user_new'

    # Act
    rename_content_type._rename(apps, connections[DEFAULT_DB_ALIAS].schema_editor(), old_model, new_model)

    # Assert
    assert ContentType.objects.filter(app_label='auth', model=new_model).count() == 0

def test_rename_content_type_integrity_error(rename_content_type):
    # Arrange
    old_model = 'user'
    new_model = 'user'  # new model is same as old, should trigger integrity error

    ContentType.objects.create(app_label='auth', model=old_model)

    # Act
    with transaction.atomic():
        rename_content_type._rename(apps, connections[DEFAULT_DB_ALIAS].schema_editor(), old_model, new_model)

    # Assert
    assert ContentType.objects.get(app_label='auth', model=old_model).model == old_model
    assert ContentType.objects.filter(app_label='auth', model=new_model).count() == 0

def test_rename_content_type_clear_cache(rename_content_type):
    # Arrange
    old_model = 'user'
    new_model = 'user_new'
    ContentType.objects.create(app_label='auth', model=old_model)

    # Act
    rename_content_type._rename(apps, connections[DEFAULT_DB_ALIAS].schema_editor(), old_model, new_model)
    
    rename_content_type._rename(apps, connections[DEFAULT_DB_ALIAS].schema_editor(), new_model, old_model)

    # Assert
    assert ContentType.objects.get(app_label='auth', model=old_model).model == old_model