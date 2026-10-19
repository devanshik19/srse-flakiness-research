import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.migrations.questioner import MigrationQuestioner
from django.db.migrations.autodetector import MigrationAutodetector
from django.db import migrations

@pytest.fixture
def simulated_states():
    # Simulating the states before and after a change
    user_field_changes = {
        'user': {
            'old_field': User._meta.get_field('username'),
            'new_field': User._meta.get_field('email'),  # Changing from username to email
        }
    }
    return user_field_changes

def test_generate_altered_fields(simulated_states):
    questioner = MigrationQuestioner()
    autodetector = MigrationAutodetector.from_states({}, {'user': User})

    autodetector.old_field_keys = {('auth', 'user', 'username')}
    autodetector.new_field_keys = {('auth', 'user', 'email')}
    autodetector.old_apps = {
        'auth': migrations.state.ModelState('auth_user', fields={'username': simulated_states['user']['old_field']})
    }
    autodetector.new_apps = {
        'auth': migrations.state.ModelState('auth_user', fields={'email': simulated_states['user']['new_field']})
    }
    
    autodetector.generate_altered_fields()

    # Verifying that the AlterField operation was added
    assert len(autodetector.ops) == 1
    operation = autodetector.ops[0]
    assert isinstance(operation, migrations.operations.models.AlterField)
    assert operation.name == 'email'
    assert operation.model_name == 'user'
    assert operation.field == simulated_states['user']['new_field']
    
    # Check that the operation is correctly set for altering a field
    assert operation.preserve_default == True