import pytest
from django.contrib.auth.models import User
from django.db import connection, models
from django.db.migrations.operations.models import CreateModel
from django.db.migrations.state import ProjectState

@pytest.fixture
def create_model_operation():
    fields = [('username', models.CharField(max_length=150, unique=True))]
    options = {}
    return CreateModel(name='CustomUser', fields=fields, options=options, bases=(User,), managers=[])

def test_database_forwards(create_model_operation):
    app_label = 'auth'
    schema_editor = connection.schema_editor()
    
    # Create a temporary state with no User model
    from_state = ProjectState()
    to_state = ProjectState()
    to_state.apps.clear()
    to_state.apps.register_model(app_label, User)

    # Run the database_forwards method
    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

    # Check if the model was created
    model = to_state.apps.get_model(app_label, create_model_operation.name)
    assert model._meta.model_name == 'customuser'
    assert 'username' in [field.name for field in model._meta.fields]

    # Clean up after test
    schema_editor.remove_model(model)