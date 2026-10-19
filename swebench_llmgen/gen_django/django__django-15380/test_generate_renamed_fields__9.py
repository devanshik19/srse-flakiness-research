import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.migrations.autodetector import MigrationAutodetector
from django.db import migrations

@pytest.fixture
def setup_migration_autodetector():
    class MockQuestioner:
        def ask_rename(self, model_name, old_field_name, new_field_name, field):
            return True  # Simulate user confirmation for renaming fields

    from_state = migrations.state.ProjectState()
    to_state = migrations.state.ProjectState()
    questioner = MockQuestioner()

    detector = MigrationAutodetector(from_state, to_state, questioner)
    return detector

def test_generate_renamed_fields(setup_migration_autodetector):
    detector = setup_migration_autodetector

    # Simulate initial models state
    old_model = migrations.state.ModelState('auth.user', {
        'id': models.AutoField(primary_key=True),
        'username': models.CharField(max_length=150, unique=True),
        'email': models.EmailField(),
    })
    new_model = migrations.state.ModelState('auth.user', {
        'id': models.AutoField(primary_key=True),
        'user_name': models.CharField(max_length=150, unique=True),  # Renamed field
        'email': models.EmailField(),
    })

    # Fill in the models into the states
    detector.from_state.models['auth.user'] = old_model
    detector.to_state.models['auth.user'] = new_model

    # Setup old and new field keys
    detector.old_field_keys = {( 'auth', 'user', 'username' )}
    detector.new_field_keys = {( 'auth', 'user', 'user_name' )}

    # This assumes renamed models are empty or not relevant for the test
    detector.renamed_models_rel = {}

    detector.generate_renamed_fields()

    # Assert the renamed fields have been detected
    assert ('auth', 'user', 'user_name') in detector.renamed_fields
    assert detector.renamed_fields[('auth', 'user', 'user_name')] == 'username'

    # Assert that the correct operations were added
    operations = detector.operations
    assert len(operations) == 2
    assert isinstance(operations[0], migrations.operations.AlterField)
    assert operations[0].name == 'username'
    assert isinstance(operations[1], migrations.operations.RenameField)
    assert operations[1].old_name == 'username'
    assert operations[1].new_name == 'user_name'