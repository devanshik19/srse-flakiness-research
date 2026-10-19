import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db import migrations

class MockQuestioner:
    def ask_rename(self, model_name, old_name, new_name, field):
        return True

@pytest.fixture
def setup_migration_autodetector():
    old_model = migrations.state.ModelState(app_label='auth', model_name='user', fields={
        'username': ('django.db.models.fields.CharField', [], {'max_length': '150', 'unique': True}),
    })
    new_model = migrations.state.ModelState(app_label='auth', model_name='user', fields={
        'username': ('django.db.models.fields.CharField', [], {'max_length': '150', 'unique': True}),
        'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': True}),
    })
    
    from_state = migrations.state.ProjectState()
    from_state.add_model(old_model)
    
    to_state = migrations.state.ProjectState()
    to_state.add_model(new_model)

    questioner = MockQuestioner()
    autodetector = MigrationAutodetector(from_state, to_state, questioner)
    
    autodetector.old_field_keys = {('auth', 'user', 'username')}
    autodetector.new_field_keys = {('auth', 'user', 'email')}
    
    return autodetector

def test_generate_renamed_fields(setup_migration_autodetector):
    autodetector = setup_migration_autodetector
    autodetector.renamed_models = {}
    autodetector.renamed_models_rel = {}
    
    autodetector.generate_renamed_fields()
    
    assert ('auth', 'user', 'email') in autodetector.renamed_fields
    assert autodetector.renamed_fields[('auth', 'user', 'email')] == 'username'
    assert len(autodetector.old_field_keys) == 0
    assert len(autodetector.new_field_keys) == 1