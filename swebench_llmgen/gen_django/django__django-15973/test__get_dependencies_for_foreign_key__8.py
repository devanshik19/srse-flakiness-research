import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ModelState
from django.db.migrations.replacement import Field

@pytest.fixture
def project_state():
    return {
        'auth': {
            'user': {
                'id': Field(
                    name='id',
                    remote_field=None,
                ),
                'profile': Field(
                    name='profile',
                    remote_field=Field(
                        model='auth.Profile',
                    ),
                ),
            }
        },
        (None, 'Profile'): {
            'user': Field(
                name='user',
                remote_field=Field(
                    model='auth.User',
                ),
            ),
        }
    }

def test_get_dependencies_for_foreign_key_with_remote_model(project_state):
    detector = MigrationAutodetector(None, None, None)
    user_field = User._meta.get_field('profile')
    
    dependencies = detector._get_dependencies_for_foreign_key('auth', 'User', user_field, project_state)

    assert dependencies == [('auth', 'Profile', None, True)]

def test_get_dependencies_for_foreign_key_with_swappable_setting(project_state):
    field = Field(
        name='custom_user',
        remote_field=Field(
            model='auth.User',
        ),
        swappable_setting='AUTH_USER_MODEL',
    )
    
    detector = MigrationAutodetector(None, None, None)

    dependencies = detector._get_dependencies_for_foreign_key('auth', 'Profile', field, project_state)

    assert dependencies == [("__setting__", "AUTH_USER_MODEL", None, True)]

def test_get_dependencies_for_foreign_key_with_through_model(project_state):
    field = Field(
        name='projects',
        remote_field=Field(
            model='auth.Profile',
            through='auth.UserProfile',
        ),
    )
    
    detector = MigrationAutodetector(None, None, None)

    dependencies = detector._get_dependencies_for_foreign_key('auth', 'User', field, project_state)

    assert dependencies == [('auth', 'Profile', None, True), ('auth', 'UserProfile', None, True)]