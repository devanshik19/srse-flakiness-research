import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations import Migration
from django.db.migrations.operations import RenameField, AlterField
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def setup_migration_states():
    class MockState:
        def __init__(self, models):
            self.models = models

        def get_field(self, field_name):
            return self.models[field_name]

    old_models = {
        ('auth', 'user'): MockState({'username': User._meta.get_field('username')}),
        ('auth', 'profile'): MockState({'user_id': User._meta.get_field('id')}),
    }

    new_models = {
        ('auth', 'user'): MockState({'username': User._meta.get_field('username'), 'email': User._meta.get_field('email')}),
        ('auth', 'profile'): MockState({'user_id': User._meta.get_field('id'), 'username': User._meta.get_field('username')}),
    }

    return MockState(old_models), MockState(new_models)

def test_generate_renamed_fields(setup_migration_states):
    old_state, new_state = setup_migration_states
    questioner = pytest.Mock()
    
    # Set up the questioner mock. This will simulate user input.
    questioner.ask_rename = lambda model_name, old_field_name, new_field_name, field: True

    autodetector = MigrationAutodetector(old_state, new_state, questioner)
    autodetector.old_field_keys = {
        ('auth', 'profile', 'user_id'),
    }
    autodetector.new_field_keys = {
        ('auth', 'profile', 'username'),
    }
    autodetector.renamed_models = {}
    autodetector.renamed_models_rel = {}

    autodetector.generate_renamed_fields()

    assert ('auth', 'profile', 'username') in autodetector.renamed_fields
    assert autodetector.renamed_fields[('auth', 'profile', 'username')] == 'user_id'
    assert len(autodetector.old_field_keys) == 0  # old_field_keys should be emptied
    assert len(autodetector.renamed_fields) == 1  # Only one rename should be recorded

    operations = autodetector.operations
    assert len(operations) == 2  # We expect two operations (RenameField and AlterField)
    assert isinstance(operations[0], AlterField)
    assert operations[0].model_name == 'profile'
    assert operations[0].name == 'user_id'
    assert isinstance(operations[1], RenameField)
    assert operations[1].model_name == 'profile'
    assert operations[1].old_name == 'user_id'
    assert operations[1].new_name == 'username'