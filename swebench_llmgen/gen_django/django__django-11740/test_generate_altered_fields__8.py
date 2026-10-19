import pytest
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def migration_autodetector():
    # Setup the MigrationAutodetector with mock data
    from_state = migrations state()
    to_state = migrations state()
    questioner = MigrationQuestioner()
    autodetector = MigrationAutodetector(from_state, to_state, questioner)
    autodetector.old_apps = from_state
    autodetector.new_apps = to_state
    return autodetector

def test_generate_altered_fields(migration_autodetector):
    # Setup initial models
    old_user_field = migration_autodetector.old_apps.get_model('auth', 'User')._meta.get_field('username')
    new_user_field = migration_autodetector.new_apps.get_model('auth', 'User')._meta.get_field('username')
    
    # Mock old and new fields
    migration_autodetector.old_field_keys = {('auth', 'User', 'username')}
    migration_autodetector.new_field_keys = {('auth', 'User', 'username')}
    migration_autodetector.old_apps.get_model = lambda app_label, model_name: User
    migration_autodetector.new_apps.get_model = lambda app_label, model_name: User
    
    # Change a field property to simulate a change
    new_user_field.blank = True
    
    migration_autodetector.generate_altered_fields()
    
    # Check that the operation was generated for the altered field
    assert len(migration_autodetector.operations) > 0
    assert isinstance(migration_autodetector.operations[0], migrations.operations.AlterField)

    # Assert the details of the operation
    alter_field_op = migration_autodetector.operations[0]
    assert alter_field_op.model_name == 'User'
    assert alter_field_op.name == 'username'
    assert alter_field_op.field.blank is True

def test_no_alteration_for_identical_fields(migration_autodetector):
    # Setup fields that are not altered
    migration_autodetector.old_field_keys = {('auth', 'User', 'username')}
    migration_autodetector.new_field_keys = {('auth', 'User', 'username')}
    
    migration_autodetector.generate_altered_fields()
    
    # Ensure no operations are generated since there are no changes
    assert len(migration_autodetector.operations) == 0