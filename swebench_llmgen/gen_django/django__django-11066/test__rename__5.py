import pytest
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.apps import apps as global_apps
from django.db import migrations
from django.contrib.auth.models import User


class RenameContentType:
    def __init__(self, app_label, old_model, new_model):
        self.app_label = app_label
        self.old_model = old_model
        self.new_model = new_model

    def _rename(self, apps, schema_editor, old_model, new_model):
        ContentType = apps.get_model('contenttypes', 'ContentType')
        db = schema_editor.connection.alias
        if not router.allow_migrate_model(db, ContentType):
            return

        try:
            content_type = ContentType.objects.db_manager(db).get_by_natural_key(self.app_label, old_model)
        except ContentType.DoesNotExist:
            pass
        else:
            content_type.model = new_model
            try:
                with transaction.atomic(using=db):
                    content_type.save(update_fields={'model'})
            except IntegrityError:
                content_type.model = old_model
            else:
                ContentType.objects.clear_cache()

def test_rename_content_type_success(schema_editor):
    # Arrange
    app_label = 'auth'
    old_model = 'user'
    new_model = 'new_user'
    content_type = ContentType.objects.create(app_label=app_label, model=old_model)
    
    rename_ct = RenameContentType(app_label, old_model, new_model)
    
    # Act
    rename_ct._rename(global_apps, schema_editor, old_model, new_model)
    
    # Assert
    content_type.refresh_from_db()
    assert content_type.model == new_model
    assert ContentType.objects.get(app_label=app_label, model=new_model) == content_type

def test_rename_content_type_does_not_exist(schema_editor):
    # Arrange
    app_label = 'auth'
    old_model = 'non_existent_model'
    new_model = 'new_name'
    
    rename_ct = RenameContentType(app_label, old_model, new_model)
    
    # Act
    rename_ct._rename(global_apps, schema_editor, old_model, new_model)
    
    # Assert
    assert ContentType.objects.filter(app_label=app_label, model=new_model).count() == 0

def test_rename_content_type_conflict(schema_editor):
    # Arrange
    app_label = 'auth'
    old_model = 'user'
    new_model = 'new_user'
    existing_content_type = ContentType.objects.create(app_label=app_label, model=new_model)
    content_type = ContentType.objects.create(app_label=app_label, model=old_model)
    
    rename_ct = RenameContentType(app_label, old_model, new_model)
    
    # Act
    rename_ct._rename(global_apps, schema_editor, old_model, new_model)
    
    # Assert
    content_type.refresh_from_db()
    assert content_type.model == old_model  # Should fallback to old model due to conflict
    assert ContentType.objects.get(app_label=app_label, model=new_model) == existing_content_type