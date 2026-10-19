import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState
from django.db.migrations.operations.models import CreateModel
from django.db.migrations.chart import Graph

@pytest.fixture
def setup_project_state():
    # Create sample ProjectState for testing
    state = ProjectState()
    user_app_label = User._meta.app_label
    state.create_models = {User._meta.label: User}
    state.relations = {
        (user_app_label, 'user'): {
            (user_app_label, 'user'): {
                'id': User._meta.fields[0],
            }
        }
    }
    return state

def test_get_dependencies_for_foreign_key(app_label='auth', model_name='user', setup_project_state):
    autodetector = MigrationAutodetector(None, None, None)
    user_field = User._meta.get_field('groups')

    dependencies = autodetector._get_dependencies_for_foreign_key(app_label, model_name, user_field, setup_project_state)
    
    assert len(dependencies) > 0
    assert dependencies[0][0] == 'auth'  # the app_label
    assert dependencies[0][1] == 'group'  # the model name for Group
    assert dependencies[0][3] == True  # should be a direct relationship

def test_get_dependencies_for_foreign_key_with_swappable_setting(setup_project_state):
    class CustomUser(models.Model):
        pass
    
    user_field = CustomUser._meta.get_field('auth_user')
    user_field.swappable_setting = 'AUTH_USER_MODEL'
    
    autodetector = MigrationAutodetector(None, None, None)
    dependencies = autodetector._get_dependencies_for_foreign_key('custom_app', 'customuser', user_field, setup_project_state)
    
    assert dependencies[0][0] == '__setting__'
    assert dependencies[0][1] == 'AUTH_USER_MODEL'