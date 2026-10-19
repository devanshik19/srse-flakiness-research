import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations import Migration
from django.db.migrations.operations.models import RenameField, AlterField

@pytest.fixture
def migration_autodetector():
    from_state = Migration("0001_initial", "auth")
    to_state = Migration("0002_auto", "auth")
    questioner = MigrationQuestioner(None)

    return MigrationAutodetector(from_state, to_state, questioner)

def test_generate_renamed_fields(migration_autodetector):
    # Setup initial state with a model that has fields
    User._meta.get_field('username').db_column = 'old_username'
    renamed_field_name = 'email'
    migration_autodetector.old_field_keys = {(User._meta.app_label, User._meta.model_name, 'username')}
    migration_autodetector.new_field_keys = {(User._meta.app_label, User._meta.model_name, renamed_field_name)}

    migration_autodetector.renamed_models = {}
    migration_autodetector.renamed_models_rel = {}
    migration_autodetector.renamed_fields = {}

    # Mock the deep_deconstruct method to return same structure as the actual field
    def mock_deconstruct(field):
        return (field.name, field.field_type, {'to': field.model} if hasattr(field, 'model') else {}, )
    
    migration_autodetector.deep_deconstruct = mock_deconstruct

    # Setup a questioner that always returns `True` for renames
    def mock_ask_rename(model_name, old_field_name, new_field_name, field):
        return True

    migration_autodetector.questioner.ask_rename = mock_ask_rename

    # Call the method under test
    migration_autodetector.generate_renamed_fields()

    # Assertions to ensure the fields are renamed correctly
    assert (User._meta.app_label, User._meta.model_name, renamed_field_name) in migration_autodetector.renamed_fields
    assert migration_autodetector.renamed_fields[(User._meta.app_label, User._meta.model_name, renamed_field_name)] == 'username'
    
    operations = migration_autodetector.operations
    assert any(isinstance(op, RenameField) for op in operations)
    
    # Check whether the field renaming operation was correctly added
    rename_operation = next(op for op in operations if isinstance(op, RenameField))
    assert rename_operation.old_name == 'username'
    assert rename_operation.new_name == renamed_field_name