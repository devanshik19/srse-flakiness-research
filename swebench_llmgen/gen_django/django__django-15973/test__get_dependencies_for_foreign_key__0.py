import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState
from django.db.migrations.utils import resolve_relation

# Create a test model to mimic foreign key relationships
class TestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

@pytest.fixture
def project_state():
    app_label = 'app_name'
    state = ProjectState()
    # Simulating a relationship in the project state
    state.relations[(app_label, 'TestModel')] = {
        (User._meta.app_label, User.__name__): {
            'user': TestModel._meta.fields[0]
        }
    }
    return state

def test_get_dependencies_for_foreign_key(project_state):
    app_label = 'app_name'
    model_name = 'TestModel'
    field = TestModel._meta.get_field('user')

    autodetector = MigrationAutodetector(None, None, None)
    dependencies = autodetector._get_dependencies_for_foreign_key(app_label, model_name, field, project_state)

    # Check if resolved dependencies include the User model
    expected_dependency = (User._meta.app_label, User.__name__, None, True)
    assert expected_dependency in dependencies
    assert len(dependencies) == 1  # Only one dependency should be present

def test_get_dependencies_for_foreign_key_with_swappable_setting(project_state):
    app_label = 'app_name'
    model_name = 'TestModel'
    
    class SwappableModel(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, swappable_setting='SwappableUser')

    field = SwappableModel._meta.get_field('user')
    
    autodetector = MigrationAutodetector(None, None, None)
    dependencies = autodetector._get_dependencies_for_foreign_key(app_label, model_name, field, project_state)

    # Check if swappable setting is correctly processed
    expected_dependency = ('__setting__', 'SwappableUser', None, True)
    assert expected_dependency in dependencies
    assert len(dependencies) == 1  # Only one dependency for swappable model