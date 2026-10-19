import pytest
from django.db import migrations
from django.contrib.auth.models import User
from django.db import connection

class TestCreateModel:
    @pytest.fixture
    def create_model_operation(self):
        return migrations.CreateModel(
            name='TestUserModel',
            fields=[('username', models.CharField(max_length=150, unique=True))],
            options={},
            bases=(User,),
            managers=None
        )

    def test_database_forwards_creates_model(self, create_model_operation):
        app_label = 'auth'
        schema_editor = connection.schema_editor()
        from_state = migrations.state.ProjectState()
        to_state = from_state.clone()
        to_state.apps.register_model(app_label, create_model_operation.name, User)

        # Pre-check: Model should not exist
        assert not create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

        # Execute the method
        create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)
        
        # Post-check: Model should exist
        model = to_state.apps.get_model(app_label, create_model_operation.name)
        assert model._meta.model_name == create_model_operation.name.lower()
        
        # Clean up: Drop the model after the test
        schema_editor.remove_model(model)

    def test_database_forwards_allows_migration(self, create_model_operation):
        app_label = 'auth'
        schema_editor = connection.schema_editor()
        from_state = migrations.state.ProjectState()
        to_state = from_state.clone()
        to_state.apps.register_model(app_label, create_model_operation.name, User)

        create_model_operation.allow_migrate_model = lambda alias, model: True

        # Execute the method
        create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)
        
        model = to_state.apps.get_model(app_label, create_model_operation.name)
        assert model._meta.model_name == create_model_operation.name.lower()

        # Clean up: Drop the model after the test
        schema_editor.remove_model(model)

    def test_database_forwards_denies_migration(self, create_model_operation):
        app_label = 'auth'
        schema_editor = connection.schema_editor()
        from_state = migrations.state.ProjectState()
        to_state = from_state.clone()
        to_state.apps.register_model(app_label, create_model_operation.name, User)

        create_model_operation.allow_migrate_model = lambda alias, model: False

        # Execute the method
        result = create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)
        
        # Ensure it does not create the model
        assert not result