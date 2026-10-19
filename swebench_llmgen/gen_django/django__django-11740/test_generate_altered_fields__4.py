import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations import operations
from django.db.migrations.autodetector import MigrationAutodetector

@pytest.fixture
def migration_autodetector():
    # Creating mock states for testing
    old_apps = apps
    new_apps = apps

    # Create a mock questioner
    class MockQuestioner:
        def ask_not_null_alteration(self, field_name, model_name):
            return 'new_default_value'

    questioner = MockQuestioner()

    return MigrationAutodetector(from_state=None, to_state=None, questioner=questioner)

def test_generate_altered_fields(migration_autodetector):
    # Setup the old and new field states
    migration_autodetector.old_field_keys = {('auth', 'user', 'username')}
    migration_autodetector.new_field_keys = {('auth', 'user', 'username')}
    migration_autodetector.old_apps = apps
    migration_autodetector.new_apps = apps

    # Prepare old and new fields
    user_model = User
    old_field = user_model._meta.get_field('username')
    migration_autodetector.deep_deconstruct = lambda field: (field.name, field.model.__name__, field.max_length)

    # Create a new field with some changes
    new_field = models.CharField(max_length=150, null=True)
    migration_autodetector.new_apps.get_model = lambda app_label, model_name: type(
        'MockModel',
        (models.Model,),
        {'_meta': type('Meta', (), {'get_field': lambda self, name: new_field})}
    )()

    # Mocking the operation to capture what is added
    migration_autodetector.add_operation = lambda app_label, operation: setattr(migration_autodetector, 'last_operation', operation)

    # Call the method under test
    migration_autodetector.generate_altered_fields()

    # Verify the operation
    assert hasattr(migration_autodetector, 'last_operation')
    assert isinstance(migration_autodetector.last_operation, operations.AlterField)
    assert migration_autodetector.last_operation.name == 'username'
    assert migration_autodetector.last_operation.field.max_length == 150

def test_generate_altered_fields_m2m(migration_autodetector):
    # Setup for many-to-many changes
    migration_autodetector.old_field_keys = {('auth', 'user', 'groups')}
    migration_autodetector.new_field_keys = {('auth', 'user', 'groups')}
    migration_autodetector.old_apps = apps
    migration_autodetector.new_apps = apps

    m2m_old_field = User._meta.get_field('groups')
    migration_autodetector.deep_deconstruct = lambda field: (field.name, field.model.__name__, field.related_model)

    # Create a new many-to-many field
    new_field = models.ManyToManyField(User)
    migration_autodetector.new_apps.get_model = lambda app_label, model_name: type(
        'MockModel',
        (models.Model,),
        {'_meta': type('Meta', (), {'get_field': lambda self, name: new_field})}
    )()

    # Mocking operation
    migration_autodetector.add_operation = lambda app_label, operation: setattr(migration_autodetector, 'last_operation', operation)

    # Call the method under test
    migration_autodetector.generate_altered_fields()

    # Check for AlterField is not created when switching to m2m
    assert not hasattr(migration_autodetector, 'last_operation')