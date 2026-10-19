import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState

@pytest.mark.parametrize("remote_field_model, expected_dependencies", [
    (User, [("__setting__", "User", None, True)]),
    ("auth.CustomUserModel", [("auth", "CustomUserModel", None, True)]),
])
def test_get_dependencies_for_foreign_key(remote_field_model, expected_dependencies):
    class ForeignKeyField(models.ForeignKey):
        def __init__(self, *args, **kwargs):
            kwargs['related_name'] = 'related_test'
            kwargs['on_delete'] = models.CASCADE
            super().__init__(remote_field_model, *args, **kwargs)

    field = ForeignKeyField()
    project_state = ProjectState()
    project_state.relations = {
        ('auth', 'User'): {
            'id': field,
        }
    }
    
    autodetector = MigrationAutodetector(None, None, None)

    dependencies = autodetector._get_dependencies_for_foreign_key('auth', 'User', field, project_state)
    
    assert dependencies == expected_dependencies


def test_get_dependencies_with_through_model():
    class ThroughModel(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='through_users')

    class ForeignKeyWithThrough(models.ForeignKey):
        def __init__(self):
            super().__init__(ThroughModel, on_delete=models.CASCADE)

    field = ForeignKeyWithThrough()
    project_state = ProjectState()
    project_state.relations = {
        ('auth', 'User'): {
            'id': field,
        }
    }
    
    autodetector = MigrationAutodetector(None, None, None)

    dependencies = autodetector._get_dependencies_for_foreign_key('auth', 'User', field, project_state)
    
    assert len(dependencies) == 2
    assert dependencies[0] == ("__setting__", "ThroughModel", None, True)
    assert dependencies[1] == ("auth", "User", None, True)