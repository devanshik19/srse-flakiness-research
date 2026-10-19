import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.state import ProjectState
from django.db.migrations.autodetector import MigrationAutodetector


class ForeignKeyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProjectStateMock:
    def __init__(self):
        self.relations = {
            ('app_label', 'ForeignKeyModel'): {
                ('auth', 'User'): { 'user': ForeignKeyModel._meta.get_field('user') },
            }
        }


@pytest.fixture
def migration_autodetector():
    return MigrationAutodetector(from_state=None, to_state=None, questioner=None)


def test_get_dependencies_for_foreign_key_with_remote_model(migration_autodetector):
    field = ForeignKeyModel._meta.get_field('user')
    app_label = 'app_label'
    model_name = 'ForeignKeyModel'
    project_state = ProjectStateMock()

    dependencies = migration_autodetector._get_dependencies_for_foreign_key(
        app_label, model_name, field, project_state
    )
    
    assert len(dependencies) == 1
    assert dependencies[0][:2] == ('auth', 'User')
    assert dependencies[0][3] is True


def test_get_dependencies_for_foreign_key_with_swappable_setting(migration_autodetector):
    field = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        swappable_setting='AUTH_USER_MODEL'
    )

    app_label = 'app_label'
    model_name = 'TestModel'
    project_state = ProjectStateMock()

    dependencies = migration_autodetector._get_dependencies_for_foreign_key(
        app_label, model_name, field, project_state
    )

    assert len(dependencies) == 1
    assert dependencies[0][:2] == ('__setting__', 'AUTH_USER_MODEL')
    assert dependencies[0][3] is True