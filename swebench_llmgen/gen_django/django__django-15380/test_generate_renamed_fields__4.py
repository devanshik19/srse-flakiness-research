import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.questioner import MigrationQuestioner
from django.db.migrations import operations
from django.db.migrations.state import ProjectState
from django.db.migrations.autodetector import MigrationAutodetector

class MockMigrationQuestioner(MigrationQuestioner):
    def ask_rename(self, model_name, old_field_name, new_field_name, field):
        return True

@pytest.fixture
def mock_states():
    old_model_state = ProjectState()
    new_model_state = ProjectState()

    old_model = MockUserModel()
    new_model = MockUserModel()

    old_model._meta.pk.attname = 'id'
    new_model._meta.pk.attname = 'id'
    
    old_model_state.add_model('auth', old_model)
    new_model_state.add_model('auth', new_model)
    
    return old_model_state, new_model_state

class MockUserModel:
    app_label = 'auth'
    model_name = 'user'
    
    @classmethod
    def get_field(cls, field_name):
        if field_name == 'renamed_field':
            return User._meta.get_field('username')
        return None
    
    def _meta(cls):
        return User._meta

def test_generate_renamed_fields(mock_states):
    old_model_state, new_model_state = mock_states

    autodetector = MigrationAutodetector(old_model_state, new_model_state, MockMigrationQuestioner())
    autodetector.old_field_keys = {('auth', 'user', 'renamed_field')}
    autodetector.new_field_keys = {('auth', 'user', 'username')}
    autodetector.renamed_models = {}
    autodetector.questioner = MockMigrationQuestioner()

    autodetector.generate_renamed_fields()

    # Check that the renamed field was detected
    assert ('auth', 'user', 'username') in autodetector.renamed_fields
    assert autodetector.renamed_fields[('auth', 'user', 'username')] == 'renamed_field'
    assert len(autodetector.old_field_keys) == 0