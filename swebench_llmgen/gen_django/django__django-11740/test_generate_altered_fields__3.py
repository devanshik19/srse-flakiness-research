import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations import operations

@pytest.fixture
def setup_migration_autodetector():
    old_user_field = User._meta.get_field('username')
    new_user_field = User._meta.get_field('email')

    old_apps = apps.get_app_config('auth').get_models()
    new_apps = apps.get_app_config('auth').get_models()

    return MigrationAutodetector(from_state=old_apps, to_state=new_apps, questioner=None)

def test_generate_altered_fields_setup(setup_migration_autodetector):
    autodetector = setup_migration_autodetector
    
    autodetector.old_field_keys = {('auth', 'user', 'username')}
    autodetector.new_field_keys = {('auth', 'user', 'email')}
    autodetector.renamed_models = {}
    autodetector.renamed_fields = {}
    autodetector.old_apps = apps
    autodetector.new_apps = apps
    
    autodetector.generate_altered_fields()

    assert len(autodetector.operations) == 1
    assert isinstance(autodetector.operations[0], operations.AlterField)
    assert autodetector.operations[0].name == 'email'
    assert autodetector.operations[0].field == new_user_field

def test_generate_altered_fields_with_not_null(setup_migration_autodetector):
    autodetector = setup_migration_autodetector

    old_field_def = 'username'
    new_field_def = 'email'
    # Simulating that old username field is nullable without default
    User._meta.get_field(old_field_def).null = True
    User._meta.get_field(old_field_def).default = models.NOT_PROVIDED

    autodetector.old_field_keys = {('auth', 'user', old_field_def)}
    autodetector.new_field_keys = {('auth', 'user', new_field_def)}
    autodetector.renamed_models = {}
    autodetector.renamed_fields = {}
    autodetector.old_apps = apps
    autodetector.new_apps = apps
    autodetector.questioner = lambda field_name, model_name: 'default_email@example.com'

    autodetector.generate_altered_fields()

    assert len(autodetector.operations) == 1
    assert isinstance(autodetector.operations[0], operations.AlterField)
    assert autodetector.operations[0].field.default == 'default_email@example.com'

def test_generate_altered_fields_multiple_scenarios(setup_migration_autodetector):
    autodetector = setup_migration_autodetector

    old_field_def = 'username'
    new_field_def = 'email'
    # Simulating the condition of changing from not-null to nullable
    User._meta.get_field(old_field_def).null = False
    User._meta.get_field(old_field_def).default = 'default_username'

    autodetector.old_field_keys = {('auth', 'user', old_field_def)}
    autodetector.new_field_keys = {('auth', 'user', new_field_def)}
    autodetector.renamed_models = {}
    autodetector.renamed_fields = {}
    autodetector.old_apps = apps
    autodetector.new_apps = apps
    
    autodetector.generate_altered_fields()

    assert len(autodetector.operations) == 1
    assert isinstance(autodetector.operations[0], operations.AlterField)
    assert autodetector.operations[0].field.default == 'default_username'

    # Clean up the conditions for next tests (if needed)
    User._meta.get_field(old_field_def).null = True
    User._meta.get_field(old_field_def).default = models.NOT_PROVIDED