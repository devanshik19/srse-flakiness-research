import pytest
from django.db import models, connection
from django.db.migrations.state import ModelState
from django.contrib.auth.models import User
from django.db.migrations.operations.models import CreateModel

@pytest.fixture
def create_model_operation():
    return CreateModel(name='TestModel', fields=[], options={}, bases=[], managers=[])

def test_database_forwards(create_model_operation):
    app_label = 'auth'
    schema_editor = connection.schema_editor()
    
    # Prepare the state before the migration
    from_state = ModelState(app_label, 'some_model', None)
    to_state = ModelState(app_label, 'TestModel', User)

    # Run database_forwards
    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

    # Verify that the model was created
    created_models = schema_editor.connection.introspection.get_model_list(schema_editor.connection.alias)
    assert 'TestModel' in created_models

    # Clean up, if necessary
    schema_editor.delete_model(User)  # clean up created user table if needed