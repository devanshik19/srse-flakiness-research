import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.migrations.autodetector import MigrationAutodetector
from django.db import migrations

@pytest.fixture
def autodetector():
    from_state = migrations.State(
        apps={'auth': ['User']},
        models={'auth.User': User}
    )
    to_state = migrations.State(
        apps={'auth': ['User']},
        models={'auth.User': User}
    )
    questioner = migrations.questioner.MigrationQuestioner()
    return MigrationAutodetector(from_state, to_state, questioner)

def test_generate_altered_fields(autodetector):
    # Setup old and new field definitions for User model
    old_user_meta = User._meta
    new_user_meta = User._meta

    # Simulate a field change by modifying a User's field
    old_apps = {
        'auth': {
            'User': old_user_meta
        }
    }
    new_apps = {
        'auth': {
            'User': new_user_meta
        }
    }

    autodetector.old_apps = old_apps
    autodetector.new_apps = new_apps
    autodetector.old_field_keys = {('auth', 'User', 'username')}
    autodetector.new_field_keys = {('auth', 'User', 'username')}
    autodetector.renamed_models = {}
    autodetector.renamed_fields = {}

    # Run the generate_altered_fields function
    autodetector.generate_altered_fields()

    # Assert that the correct operations are added
    assert len(autodetector.operations) > 0

    # Check if the generated operation is of type AlterField
    assert isinstance(autodetector.operations[0], migrations.AlterField)

    # Assert specific details about the AlterField operation
    operation = autodetector.operations[0]
    assert operation.model_name == 'User'
    assert operation.name == 'username'
    assert operation.field.__class__ == User._meta.get_field('username').__class__