import pytest
from django.db import models, connection
from django.db.migrations.state import ProjectState
from django.contrib.auth.models import User
from django.db.migrations.operations.models import CreateModel

@pytest.fixture
def create_model_operation():
    return CreateModel(
        name='User',
        fields=[
            ('username', models.CharField(max_length=150, unique=True)),
            ('email', models.EmailField(unique=True)),
        ],
        options={},
        bases=(models.Model,),
        managers=None
    )

def test_database_forwards(create_model_operation):
    app_label = 'auth'
    schema_editor = connection.schema_editor()
    
    # Create a state before the migration
    from_state = ProjectState()
    to_state = ProjectState()
    
    # Run the migration forwards
    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)
    
    # Check if the model was created in the database
    user_model = to_state.apps.get_model(app_label, 'User')
    assert user_model.objects.exists()
    
    # Verify the attributes of the created model
    user_instance = user_model(username='testuser', email='testuser@example.com')
    user_instance.save()
    
    assert user_model.objects.filter(username='testuser').exists()
    assert user_model.objects.filter(email='testuser@example.com').exists()
    
    # Clean up the user instance
    user_instance.delete()

    # Test that the model is not allowed to be migrated again to verify branch coverage
    assert not create_model_operation.allow_migrate_model(schema_editor.connection.alias, user_model)