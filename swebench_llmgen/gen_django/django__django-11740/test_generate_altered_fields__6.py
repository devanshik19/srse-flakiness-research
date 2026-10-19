import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations import operations

@pytest.fixture
def setup_migration_autodetector():
    old_field = models.CharField(max_length=100, null=True)
    new_field = models.CharField(max_length=150, null=False)
    
    old_apps = {
        'auth': {
            'User': type('OldUser', (User,), {
                'my_field': old_field
            })
        }
    }
    
    new_apps = {
        'auth': {
            'User': type('NewUser', (User,), {
                'my_field': new_field
            })
        }
    }
    
    autodetector = MigrationAutodetector(old_apps, new_apps, None)
    autodetector.old_field_keys = {('auth', 'User', 'my_field')}
    autodetector.new_field_keys = {('auth', 'User', 'my_field')}
    autodetector.renamed_fields = {}
    autodetector.renamed_models = {}
    autodetector.questioner = operations.Questioner()
    return autodetector

def test_generate_altered_fields(setup_migration_autodetector):
    autodetector = setup_migration_autodetector
    autodetector.generate_altered_fields()

    operations_list = autodetector.operations
    assert len(operations_list) == 1
    assert isinstance(operations_list[0], operations.AlterField)
    assert operations_list[0].model_name == 'User'
    assert operations_list[0].name == 'my_field'
    assert operations_list[0].field.max_length == 150
    assert operations_list[0].preserve_default is True