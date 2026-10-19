import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.db.migrations.state import ProjectState
from django.db.migrations.operations.models import CreateModel

def test_database_forwards():
    # Setup
    name = 'MyModel'
    fields = [('field1', models.CharField(max_length=10))]
    options = {}
    bases = (models.Model,)
    managers = []
    
    create_model_operation = CreateModel(name, fields, options, bases, managers)
    
    # Prepare states
    from_state = ProjectState()
    to_state = ProjectState()
    to_state.add_model(name, fields)
    
    # Create schema editor to execute the operation
    schema_editor = connection.schema_editor()
    
    # Act
    create_model_operation.database_forwards('auth', schema_editor, from_state, to_state)
    
    # Assert
    # Check if the model exists
    model = to_state.apps.get_model('auth', name)
    assert model.objects.exists() is False  # No instances should exist right after creation

    # Ensure the model has been created
    assert model._meta.model_name == name.lower()
    assert hasattr(model, 'field1')
    
    # Cleanup
    schema_editor.remove_model(model)