import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState

@pytest.fixture
def project_state():
    # Mimic the ProjectState with relationships for testing
    state = ProjectState()
    state.relations = {
        ("auth", "user"): {
            ("auth", "profile"): {
                "user": models.ForeignKey(User, on_delete=models.CASCADE)
            }
        }
    }
    return state

def test_get_dependencies_for_foreign_key_with_direct_relation(project_state):
    # Arrange
    detector = MigrationAutodetector(None, None, None)
    user_field = User._meta.get_field("username")

    # Act
    dependencies = detector._get_dependencies_for_foreign_key("auth", "user", user_field, project_state)

    # Assert
    assert dependencies == [('auth', 'profile', None, True)]

def test_get_dependencies_for_foreign_key_with_swappable_setting(project_state):
    # Arrange
    class MyModel(models.Model):
        my_field = models.ForeignKey('auth.User', swappable_setting='AUTH_USER_MODEL', on_delete=models.CASCADE)
    
    detector = MigrationAutodetector(None, None, None)
    my_field = MyModel._meta.get_field("my_field")

    # Act
    dependencies = detector._get_dependencies_for_foreign_key("myapp", "mymodel", my_field, project_state)

    # Assert
    assert dependencies == [("__setting__", "AUTH_USER_MODEL", None, True)]

def test_get_dependencies_for_foreign_key_with_through_model(project_state):
    # Arrange
    class Profile(models.Model):
        user = models.ForeignKey(User, related_name='profiles', on_delete=models.CASCADE)

    class UserProfile(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    detector = MigrationAutodetector(None, None, None)
    user_field = UserProfile._meta.get_field("profile")

    # Act
    dependencies = detector._get_dependencies_for_foreign_key("myapp", "userprofile", user_field, project_state)

    # Assert
    assert len(dependencies) == 2
    assert dependencies[0] == ('auth', 'user', None, True)  # dependency on User model
    assert dependencies[1] == ('auth', 'profile', None, True)  # dependency on Profile model