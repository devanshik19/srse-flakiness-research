import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations.models import CreateModel
from django.db.migrations.state import ModelState

class TestCreateModel:
    def setup_method(self):
        # Create a mock schema_editor
        self.schema_editor = models.schema_editor()
        self.name = 'User'
        self.fields = {
            'username': models.CharField(max_length=150),
            'password': models.CharField(max_length=128),
            'email': models.EmailField(unique=True),
            'first_name': models.CharField(max_length=30, blank=True),
            'last_name': models.CharField(max_length=30, blank=True),
        }
        self.options = {}
        self.bases = (models.Model,)
        self.create_model_operation = CreateModel(self.name, self.fields, self.options, self.bases, [])

    @pytest.mark.parametrize("allow_migrate", [True, False])
    def test_database_forwards(self, allow_migrate):
        app_label = 'auth'
        from_state = ModelState(app_label, 'User', {})
        to_state = ModelState(app_label, 'User', self.fields)

        # Mock the allow_migrate_model method
        def allow_migrate_model(alias, model):
            return allow_migrate

        self.create_model_operation.allow_migrate_model = allow_migrate_model

        # Execute the method
        if allow_migrate:
            self.create_model_operation.database_forwards(app_label, self.schema_editor, from_state, to_state)
            # Check if model was created in the database
            assert self.schema_editor.model_exists(app_label, 'User')
        else:
            with pytest.raises(Exception, match="Migration not allowed"):
                self.create_model_operation.database_forwards(app_label, self.schema_editor, from_state, to_state)