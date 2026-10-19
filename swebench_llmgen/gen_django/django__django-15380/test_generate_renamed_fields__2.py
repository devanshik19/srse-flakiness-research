import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations import Migration
from django.db.migrations.operations.models import RenameField, AlterField
from django.db.migrations.autodetector import MigrationAutodetector

class MockQuestioner:
    def ask_rename(self, model_name, old_field_name, new_field_name, field):
        return True

@pytest.fixture
def setup_migration_autodetector():
    # Create a mock state to mimic the from_state and to_state
    class MockModelState:
        def __init__(self, model_name, field_name, db_column):
            self.model_name = model_name
            self.fields = {field_name: MockField(field_name, db_column)}

        def get_field(self, field_name):
            return self.fields[field_name]

    class MockField:
        def __init__(self, name, db_column):
            self.name = name
            self.db_column = db_column
            self.remote_field = None

        def get_attname_column(self):
            return (self.name, self.db_column)

        def set_attributes_from_name(self, name):
            self.name = name

        def clone(self):
            return MockField(self.name, self.db_column)

    from_state = Migration(None, '0001_initial')
    to_state = Migration(None, '0002_auto')

    from_state.models = {
        ('auth', 'user'): MockModelState('User', 'old_field', 'old_field_db')
    }

    to_state.models = {
        ('auth', 'user'): MockModelState('User', 'new_field', 'new_field_db')
    }

    autodetector = MigrationAutodetector(from_state, to_state, MockQuestioner())
    autodetector.old_field_keys = {('auth', 'user', 'old_field')}
    autodetector.new_field_keys = {('auth', 'user', 'new_field')}
    autodetector.renamed_models = {}

    return autodetector

def test_generate_renamed_fields(setup_migration_autodetector):
    autodetector = setup_migration_autodetector
    autodetector.generate_renamed_fields()

    assert ('auth', 'user', 'new_field') in autodetector.renamed_fields
    assert autodetector.renamed_fields[('auth', 'user', 'new_field')] == 'old_field'
    assert len(autodetector.old_field_keys) == 0  # old_field should be removed
    assert len(autodetector.renamed_fields) == 1