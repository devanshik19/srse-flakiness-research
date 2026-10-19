import pytest
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.operations.models import RenameField, AlterField
from django.contrib.auth.models import User
from django.db.migrations.state import ProjectState


class MockQuestioner:
    def ask_rename(self, model_name, old_field_name, new_field_name, field):
        return True  # Simulate user saying "yes" to renaming


@pytest.fixture
def setup_migration_autodetector():
    # Create mock ProjectState
    old_user_state = ProjectState()
    old_user_state.apps.register_model('auth', User)
    old_user_state = old_user_state.clone()

    new_user_state = ProjectState()
    new_user_state.apps.register_model('auth', User)
    new_user_state = new_user_state.clone()

    old_fields = {('auth', 'user', 'username'), ('auth', 'user', 'email')}
    new_fields = {('auth', 'user', 'user_name'), ('auth', 'user', 'email')}  # Assume username changed to user_name

    old_user = old_user_state.models['auth', 'user']
    new_user = new_user_state.models['auth', 'user']
    
    old_user._meta.get_field('username').db_column = 'old_username'
    new_user._meta.get_field('user_name').db_column = 'new_user_name'

    autodetector = MigrationAutodetector(old_user_state, new_user_state, MockQuestioner())
    autodetector.old_field_keys = old_fields
    autodetector.new_field_keys = new_fields
    autodetector.renamed_models_rel = {}
    autodetector.renamed_models = {}
    autodetector.renamed_fields = {}

    return autodetector


def test_generate_renamed_fields(setup_migration_autodetector):
    autodetector = setup_migration_autodetector
    autodetector.generate_renamed_fields()

    assert ('auth', 'user', 'user_name') in autodetector.renamed_fields
    assert autodetector.renamed_fields[('auth', 'user', 'user_name')] == 'username'

    assert len(autodetector.old_field_keys) == 1  # 'email' should remain, 'username' should be removed
    assert ('auth', 'user', 'username') not in autodetector.old_field_keys
    assert ('auth', 'user', 'email') in autodetector.old_field_keys

    assert len(autodetector.operations) == 2  # Should have two operations: RenameField and AlterField
    assert isinstance(autodetector.operations[0], RenameField)
    assert isinstance(autodetector.operations[1], AlterField)
    assert autodetector.operations[0].old_name == 'username'
    assert autodetector.operations[0].new_name == 'user_name'