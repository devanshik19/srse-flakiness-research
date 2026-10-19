import pytest
from django.db import models, migrations
from django.contrib.auth.models import User

from django.db.migrations.operations.models import CreateModel

@pytest.fixture
def create_model_operation():
    fields = [('field1', models.CharField(max_length=100))]
    options = {}
    return CreateModel(name='TestModel', fields=fields, options=options, bases=(models.Model,), managers=[])

def test_database_forwards(create_model_operation):
    app_label = 'auth'
    schema_editor = migrations.schema_editor()
    from_state = migrations.state.ProjectState()
    to_state = migrations.state.ProjectState()
    
    # Set the model in the to_state
    to_state.apps.create_model(create_model_operation.name, fields=create_model_operation.fields, bases=(models.Model,))
    
    # Run the database_forwards
    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

    # Check if the model is created in the database
    assert create_model_operation.name in schema_editor.connection.introspection.get_table_list(schema_editor.connection.cursor())