import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations import CreateModel, AddField, AlterUniqueTogether
from django.db.migrations.state import ProjectState
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def setup_migration_autodetector():
    # Create a dummy from_state and to_state for migration autodetector
    old_state = ProjectState()
    new_state = ProjectState()

    # Example models to simulate state for the test
    class ExampleModel(models.Model):
        name = models.CharField(max_length=100)

    old_keys = {('app_label', 'ExampleModel')}
    new_keys = {('app_label', 'ExampleModel')}
    
    # Create the migration autodetector instance
    autodetector = MigrationAutodetector(from_state=old_state, to_state=new_state, questioner=None)
    autodetector.old_model_keys = old_keys
    autodetector.new_model_keys = new_keys
    autodetector.old_unmanaged_keys = set()
    autodetector.new_unmanaged_keys = set()
    autodetector.to_state = new_state
    autodetector.new_apps = new_state.apps

    return autodetector

def test_generate_created_models(setup_migration_autodetector):
    autodetector = setup_migration_autodetector
    autodetector.generate_created_models()

    # Validate operations created
    operations = autodetector._operations['app_label']
    assert len(operations) > 0  # Ensure that operations were added

    # Check if the correct operations are added for the ExampleModel creation
    create_model_op = operations[0]
    assert isinstance(create_model_op, CreateModel)
    assert create_model_op.name == 'ExampleModel'

    # Verify if fields are added correctly
    fields = create_model_op.fields
    assert 'name' in dict(fields)  # Check the presence of 'name' field

    # Check if operations related to unique constraints are handled
    # Here we assume that unique_together should not exist since it was not set
    assert not any(isinstance(op, AlterUniqueTogether) for op in operations)