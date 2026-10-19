import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations import RenameField, AlterField
from django.db.migrations.state import ProjectState
from django.db.migrations.questioner import MigrationQuestioner
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def migration_autodetector():
    from_state = ProjectState()
    to_state = ProjectState()
    questioner = MigrationQuestioner()
    
    autodetector = MigrationAutodetector(from_state, to_state, questioner)
    autodetector.old_field_keys = set()
    autodetector.new_field_keys = set()
    autodetector.renamed_models = {}
    autodetector.renamed_models_rel = {}
    autodetector.renamed_fields = {}
    return autodetector

def test_generate_renamed_fields(migration_autodetector):
    old_user_field = models.CharField(max_length=100, name='old_username')
    new_user_field = models.CharField(max_length=100, name='new_username')
    
    # Simulate old and new states
    migration_autodetector.from_state.models['auth.User'] = ProjectState()
    migration_autodetector.to_state.models['auth.User'] = ProjectState()
    migration_autodetector.from_state.models['auth.User'].fields = {'old_username': old_user_field}
    migration_autodetector.to_state.models['auth.User'].fields = {'new_username': new_user_field}
    
    migration_autodetector.old_field_keys.add(('auth', 'User', 'old_username'))
    migration_autodetector.new_field_keys.add(('auth', 'User', 'new_username'))

    # Setting up questioner to simulate user input
    def mock_ask_rename(model_name, old_field_name, new_field_name, field):
        return True  # Simulating a 'yes' response

    migration_autodetector.questioner.ask_rename = mock_ask_rename

    # Call the method
    migration_autodetector.generate_renamed_fields()

    # Assertions
    assert ('auth', 'User', 'new_username') in migration_autodetector.old_field_keys
    assert ('auth', 'User', 'new_username') in migration_autodetector.renamed_fields
    assert migration_autodetector.renamed_fields[('auth', 'User', 'new_username')] == 'old_username'
    assert len(migration_autodetector.renamed_fields) == 1
    assert isinstance(migration_autodetector.operations[0], RenameField)
    assert isinstance(migration_autodetector.operations[1], AlterField)