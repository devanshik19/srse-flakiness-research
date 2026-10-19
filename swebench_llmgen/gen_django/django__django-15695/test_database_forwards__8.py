import pytest
from django.db import models, connection
from django.db.migrations.operations.models import CreateModel
from django.db.migrations.state import ModelState
from django.contrib.auth.models import User

@pytest.fixture
def create_model_operation():
    return CreateModel(name='TestModel', fields=[('field1', models.CharField(max_length=100))], options={}, bases=(models.Model,), managers=[])

def test_database_forwards(create_model_operation):
    app_label = 'auth'
    schema_editor = connection.schema_editor()
    
    # Create a hypothetical state for the model
    from_state = ModelState('auth', 'User', [])
    to_state = ModelState('auth', 'TestModel', [('field1', models.CharField(max_length=100))])
    
    # Ensure the model does not exist initially
    assert not connection.introspection.table_names().contains('auth_testmodel')

    # Run the database_forwards method
    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

    # Verify the model was created
    assert 'auth_testmodel' in connection.introspection.table_names()
    assert 'field1' in connection.introspection.get_field_names('auth_testmodel')
    
    # Clean up
    schema_editor.remove_model(app_label, 'TestModel')