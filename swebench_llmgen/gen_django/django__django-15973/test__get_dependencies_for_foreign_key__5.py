import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations import Migration
from django.db.migrations.state import ProjectState
from django.db.migrations.autodetector import MigrationAutodetector

class ForeignKeyTestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

@pytest.fixture
def project_state():
    state = ProjectState()
    state.apps.register_models('app_label', [ForeignKeyTestModel])
    return state

def test_get_dependencies_for_foreign_key_with_model(project_state):
    autodetector = MigrationAutodetector(None, None, None)
    field = ForeignKeyTestModel._meta.get_field('user')
    dependencies = autodetector._get_dependencies_for_foreign_key('app_label', 'foreignkeytestmodel', field, project_state)
    
    assert len(dependencies) == 1
    assert dependencies[0] == ('auth', 'user', None, True)

def test_get_dependencies_for_foreign_key_with_swappable_setting(project_state):
    class CustomUser(models.Model):
        pass

    ForeignKeyTestModel.user = models.ForeignKey(
        'app_label.CustomUser',
        on_delete=models.CASCADE,
        swappable_setting='AUTH_USER_MODEL'
    )
    
    autodetector = MigrationAutodetector(None, None, None)
    field = ForeignKeyTestModel._meta.get_field('user')
    dependencies = autodetector._get_dependencies_for_foreign_key('app_label', 'foreignkeytestmodel', field, project_state)
    
    assert len(dependencies) == 1
    assert dependencies[0] == ('__setting__', 'AUTH_USER_MODEL', None, True)

def test_get_dependencies_for_foreign_key_with_through_model(project_state):
    class RelatedModel(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)

    class IntermediateModel(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        related = models.ForeignKey(RelatedModel, on_delete=models.CASCADE, through='IntermediateModel')

    ForeignKeyTestModel.user = models.ForeignKey(
        IntermediateModel,
        on_delete=models.CASCADE,
        related_name='foreignkeytestmodel'
    )
    
    autodetector = MigrationAutodetector(None, None, None)
    field = ForeignKeyTestModel._meta.get_field('user')
    dependencies = autodetector._get_dependencies_for_foreign_key('app_label', 'foreignkeytestmodel', field, project_state)
    
    assert len(dependencies) == 2
    assert dependencies[0] == ('app_label', 'intermediatemodel', None, True)
    assert dependencies[1] == ('auth', 'user', None, True)