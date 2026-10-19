import pytest
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.apps import apps as global_apps

from django.contrib.contenttypes.management import RenameContentType


@pytest.mark.django_db
def test_rename_content_type_success():
    # Arrange
    old_model = 'user'
    new_model = 'renamed_user'
    app_label = 'auth'
    
    # Create the content type for the User model
    user_content_type = ContentType.objects.create(app_label=app_label, model=old_model)
    
    rename_content_type = RenameContentType(app_label, old_model, new_model)
    
    # Act
    rename_content_type._rename(global_apps, user_content_type._state.db, old_model, new_model)
    
    # Assert
    ct = ContentType.objects.get(pk=user_content_type.pk)
    assert ct.model == new_model


@pytest.mark.django_db
def test_rename_content_type_does_not_exist():
    # Arrange
    old_model = 'non_existent_model'
    new_model = 'renamed_model'
    app_label = 'auth'
    
    rename_content_type = RenameContentType(app_label, old_model, new_model)
    
    # Act
    rename_content_type._rename(global_apps, DEFAULT_DB_ALIAS, old_model, new_model)
    
    # Assert
    assert ContentType.objects.filter(app_label=app_label, model=new_model).count() == 0


@pytest.mark.django_db
def test_rename_content_type_conflict():
    # Arrange
    old_model = 'user'
    new_model = 'renamed_user'
    app_label = 'auth'
    
    # Create the content type for the User model
    user_content_type = ContentType.objects.create(app_label=app_label, model=old_model)
    
    # Create a conflicting content type with the new model name
    ContentType.objects.create(app_label=app_label, model=new_model)
    
    rename_content_type = RenameContentType(app_label, old_model, new_model)
    
    # Act
    rename_content_type._rename(global_apps, user_content_type._state.db, old_model, new_model)
    
    # Assert
    ct = ContentType.objects.get(pk=user_content_type.pk)
    assert ct.model == old_model  # Should fall back to old_model due to conflict