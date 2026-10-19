import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.state import ProjectState
from django.db.migrations.operations.models import CreateModel

class TestCreateModel:

    def test_database_forwards_creates_model(self):
        schema_editor = connections['default'].schema_editor()
        from_state = ProjectState()
        to_state = ProjectState()
        
        # Create a CreateModel instance
        create_model_operation = CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(User, on_delete=models.CASCADE)),
                ('bio', models.TextField(blank=True)),
            ],
            options={},
            bases=[],
            managers=[],
        )

        # Simulate the state containing the new model
        to_state.models['myapp.UserProfile'] = create_model_operation.fields
        
        # Call database_forwards
        create_model_operation.database_forwards('myapp', schema_editor, from_state, to_state)

        # Verify the model was created
        assert 'myapp_userprofile' in schema_editor.connection.introspection.table_names()

    def test_database_forwards_does_not_create_if_not_allowed(self):
        schema_editor = connections['default'].schema_editor()
        from_state = ProjectState()
        to_state = ProjectState()
        
        # Create a CreateModel instance with allow_migrate_model returning False
        create_model_operation = CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(User, on_delete=models.CASCADE)),
                ('bio', models.TextField(blank=True)),
            ],
            options={},
            bases=[],
            managers=[],
        )
        
        # Overriding the method to simulate should not allow migration
        create_model_operation.allow_migrate_model = lambda alias, model: False
        
        # Simulate the state containing the new model
        to_state.models['myapp.UserProfile'] = create_model_operation.fields
        
        # Call database_forwards
        create_model_operation.database_forwards('myapp', schema_editor, from_state, to_state)

        # Verify the model was not created
        assert 'myapp_userprofile' not in schema_editor.connection.introspection.table_names()