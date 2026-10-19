import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState
from django.db.migrations.utils import resolve_relation


class TestMigrationAutodetector:

    @pytest.fixture
    def setup_migration_autodetector(self):
        from_state = ProjectState(project_id='test')
        to_state = ProjectState(project_id='test')
        self.detector = MigrationAutodetector(from_state, to_state, None)

    def test_get_dependencies_for_foreign_key_with_existing_model(self, setup_migration_autodetector):
        user_field = User._meta.get_field('groups')
        app_label = 'auth'
        model_name = 'user'
        project_state = ProjectState()

        # Simulating a basic project state with a related model
        project_state.models[(app_label, model_name)] = User
        dependencies = self.detector._get_dependencies_for_foreign_key(app_label, model_name, user_field, project_state)

        assert dependencies == [(app_label, 'group', None, True)]

    def test_get_dependencies_for_foreign_key_with_swappable_model(self, setup_migration_autodetector):
        class TestModel(models.Model):
            user = models.ForeignKey(User, swappable_setting='auth.User', on_delete=models.CASCADE)

        user_field = TestModel._meta.get_field('user')
        app_label = 'testapp'
        model_name = 'testmodel'
        project_state = ProjectState()
        project_state.models[(app_label, model_name)] = TestModel

        dependencies = self.detector._get_dependencies_for_foreign_key(app_label, model_name, user_field, project_state)
        
        assert dependencies == [("__setting__", "auth.User", None, True)]

    def test_get_dependencies_for_foreign_key_with_through_model(self, setup_migration_autodetector):
        class TestModel(models.Model):
            users = models.ManyToManyField(User, through='UserGroup')

        class UserGroup(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
            group = models.ForeignKey('auth.Group', on_delete=models.CASCADE)

        user_field = TestModel._meta.get_field('users')
        app_label = 'testapp'
        model_name = 'testmodel'
        project_state = ProjectState()
        project_state.models[(app_label, model_name)] = TestModel
        project_state.models[('auth', 'group')] = None

        dependencies = self.detector._get_dependencies_for_foreign_key(app_label, model_name, user_field, project_state)

        assert len(dependencies) == 2
        assert dependencies[0] == ('auth', 'group', None, True)
        assert dependencies[1] == ('auth', 'usergroup', None, True)