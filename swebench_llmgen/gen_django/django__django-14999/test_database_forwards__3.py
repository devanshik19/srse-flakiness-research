import pytest
from django.db import models, connections
from django.db.migrations.operations.models import CreateModel
from django.db.migrations.state import ProjectState
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_database_forwards():
    # Create an instance of CreateModel
    create_model_operation = CreateModel(name='TestModel', fields=[], options={}, bases=[], managers=[])

    # Simulate the app label and schema editor
    app_label = 'auth'
    schema_editor = connections['default'].schema_editor()

    # Create initial and target states
    from_state = ProjectState()
    to_state = ProjectState()
    
    # Register the User model as if it's being migrated
    to_state.apps.register_model(app_label, User)
    
    # Check that the model does not exist before the operation
    assert not create_model_operation.name in to_state.apps.all_models[app_label]
    
    # Run the database_forwards method
    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

    # Check that the model exists after the operation
    assert create_model_operation.name in to_state.apps.all_models[app_label]
    
    # Verify that the model can be accessed from the database
    created_model = to_state.apps.get_model(app_label, create_model_operation.name)
    assert created_model.objects.exists() is True