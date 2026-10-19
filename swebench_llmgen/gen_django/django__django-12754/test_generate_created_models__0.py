import pytest
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db import migrations

@pytest.fixture
def migration_autodetector():
    from_state = migrations.Migration("0001_initial", "app_name")
    to_state = migrations.Migration("0002_auto", "app_name")
    return MigrationAutodetector(from_state, to_state, None)

def test_generate_created_models(migration_autodetector):
    # Setup initial states
    migration_autodetector.old_model_keys = set()
    migration_autodetector.new_model_keys = {('app_name', 'User')}
    migration_autodetector.old_unmanaged_keys = set()
    migration_autodetector.new_unmanaged_keys = set()
    migration_autodetector.to_state.models = {
        ('app_name', 'User'): models.get_model('auth', 'User')._state
    }
    migration_autodetector.new_apps = migrations.State()
    migration_autodetector.new_apps.apps = {"auth": models.get_model('auth', 'User')}

    # Execute the method
    migration_autodetector.generate_created_models()

    # Assertions to check if expected operations were added
    assert len(migration_autodetector.operations) > 0
    assert any(isinstance(op, migrations.operations.CreateModel) for op in migration_autodetector.operations)
    user_create_model_op = next(op for op in migration_autodetector.operations if isinstance(op, migrations.operations.CreateModel))
    
    # Validate the output of the created model operation
    assert user_create_model_op.name == 'User'
    assert user_create_model_op.fields  # Ensure fields are present
    assert user_create_model_op.options == {}  # Ensure options are as expected
    assert user_create_model_op.bases == []  # Ensure bases are empty as it's a User model
    
    # Additionally, test that it does not add unmanaged models
    migration_autodetector.new_model_keys = {('app_name', 'UnmanagedModel')}
    migration_autodetector.to_state.models[('app_name', 'UnmanagedModel')] = type('UnmanagedModel', (models.Model,), {'__module__': 'app_name'})
    migration_autodetector.generate_created_models()
    assert not any(isinstance(op, migrations.operations.CreateModel) for op in migration_autodetector.operations if op.name == 'UnmanagedModel')