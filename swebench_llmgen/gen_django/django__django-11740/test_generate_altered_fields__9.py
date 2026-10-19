import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db import migrations

class MockQuestioner:
    def ask_not_null_alteration(self, field_name, model_name):
        return 'default value'

@pytest.fixture
def migration_autodetector():
    from_state = migrations.Migration("0001_initial", "app_label")
    to_state = migrations.Migration("0002_auto", "app_label")
    questioner = MockQuestioner()
    return MigrationAutodetector(from_state, to_state, questioner)

def create_user_field(name, null=False, default=None):
    return models.CharField(max_length=30, null=null, default=default)

def test_generate_altered_fields(migration_autodetector):
    # Setup old and new user model fields
    old_user_field = create_user_field(name='username', null=True)
    new_user_field = create_user_field(name='username', null=False, default='default_value')

    migration_autodetector.old_field_keys = {('auth', 'user', 'username')}
    migration_autodetector.new_field_keys = {('auth', 'user', 'username')}
    
    migration_autodetector.old_apps = {
        "app_label": migrations.state.StateApps(),
    }
    migration_autodetector.new_apps = {
        "app_label": migrations.state.StateApps(),
    }

    migration_autodetector.old_apps["app_label"].register_models('auth', User)
    migration_autodetector.new_apps["app_label"].register_models('auth', User)

    # Specify how the fields have changed
    migration_autodetector.deep_deconstruct = lambda obj: (obj.name, obj.null, obj.default)

    migration_autodetector.generate_altered_fields()

    assert len(migration_autodetector.operations) == 1
    operation = migration_autodetector.operations[0]
    assert isinstance(operation, migrations.operations.AlterField)
    assert operation.name == 'username'
    assert operation.field.null is False
    assert operation.field.default == 'default_value'