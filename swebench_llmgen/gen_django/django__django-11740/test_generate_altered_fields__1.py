import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations import operations
from unittest.mock import MagicMock


@pytest.fixture
def migration_autodetector():
    old_state = MagicMock()
    new_state = MagicMock()
    questioner = MagicMock()

    old_state.get_model.return_value._meta.get_field.side_effect = lambda x: User._meta.get_field(x)
    new_state.get_model.return_value._meta.get_field.side_effect = lambda x: User._meta.get_field(x)

    autodetector = MigrationAutodetector(from_state=old_state, to_state=new_state, questioner=questioner)
    autodetector.old_field_keys = {('auth', 'user', 'username')}
    autodetector.new_field_keys = {('auth', 'user', 'username')}
    autodetector.renamed_models = {}
    autodetector.renamed_fields = {}
    autodetector.old_apps = old_state
    autodetector.new_apps = new_state
    return autodetector


def test_generate_altered_fields(migration_autodetector):
    # Simulate a field change
    old_field = User._meta.get_field('username')
    new_field = User._meta.get_field('username')
    
    # Update properties to simulate an alteration
    new_field.null = False
    old_field.null = True

    migration_autodetector.add_operation = MagicMock()

    migration_autodetector.generate_altered_fields()

    assert migration_autodetector.add_operation.called
    called_args = migration_autodetector.add_operation.call_args[0]
    assert isinstance(called_args[1], operations.AlterField)
    assert called_args[1].model_name == 'user'
    assert called_args[1].name == 'username'
    assert called_args[1].field.null is False
    assert called_args[1].preserve_default is True

    # Now simulate changing to a many-to-many field
    new_field.many_to_many = True
    old_field.many_to_many = False

    migration_autodetector._generate_removed_field = MagicMock()
    migration_autodetector._generate_added_field = MagicMock()

    migration_autodetector.generate_altered_fields()

    assert migration_autodetector._generate_removed_field.called
    assert migration_autodetector._generate_added_field.called