import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations import operations
from django.db.migrations.state import ProjectState

@pytest.fixture
def autodetector():
    old_state = ProjectState()
    new_state = ProjectState()
    questioner = None  # Assume using the default questioner
    return MigrationAutodetector(old_state, new_state, questioner)

def test_generate_altered_fields(autodetector):
    # Setup old and new models with altered fields
    old_user = User._meta.get_field('email')
    new_field = User._meta.get_field('email').__class__(model=User, name='email', verbose_name='Email',
                                                          max_length=254, null=True, blank=True)  # Simulate alteration
    autodetector.old_apps = old_user.model.__class__._meta.apps
    autodetector.new_apps = User._meta.apps
    autodetector.old_field_keys = {(User._meta.app_label, User._meta.model_name, 'email')}
    autodetector.new_field_keys = {(User._meta.app_label, User._meta.model_name, 'email')}
    
    # Renaming mechanism (no renames in this case)
    autodetector.renamed_models = {}
    autodetector.renamed_fields = {}
    
    # Call the focal function
    autodetector.generate_altered_fields()

    # Ensure AlterField operation was created
    assert len(autodetector.old_field_keys) == len(autodetector.new_field_keys)
    assert len(autodetector.operations) == 1
    assert isinstance(autodetector.operations[0], operations.AlterField)
    assert autodetector.operations[0].model_name == User._meta.model_name
    assert autodetector.operations[0].name == 'email'
    assert autodetector.operations[0].field.null is True