import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.questioner import MigrationQuestioner
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations import operations
from django.db.migrations.state import ProjectState


class MockQuestioner(MigrationQuestioner):
    def ask_rename(self, model_name, old_field_name, new_field_name, field):
        return True


@pytest.fixture
def setup_migration_autodetector():
    questioner = MockQuestioner()
    from_state = ProjectState()
    to_state = ProjectState()
    
    old_user = User._meta.get_field('username')
    new_user = old_user.clone()
    new_user.name = 'new_username'
    
    from_state.add_model('auth', 'User', User._meta.get_fields())
    to_state.add_model('auth', 'User', [new_user] + User._meta.get_fields()[1:])

    autodetector = MigrationAutodetector(from_state, to_state, questioner)
    autodetector.old_field_keys = {(User._meta.app_label, 'User', old_user.name)}
    autodetector.new_field_keys = {(User._meta.app_label, 'User', new_user.name)}
    
    return autodetector


def test_generate_renamed_fields(setup_migration_autodetector):
    autodetector = setup_migration_autodetector
    autodetector.renamed_models = {}
    autodetector.renamed_models_rel = {}
    
    autodetector.generate_renamed_fields()
    
    assert ('auth', 'User', 'new_username') in autodetector.renamed_fields
    assert autodetector.renamed_fields[('auth', 'User', 'new_username')] == 'username'
    assert len(autodetector.old_field_keys) == 0  # old field keys should be empty after renaming
    assert len(autodetector.new_field_keys) == 1  # one new field key remains