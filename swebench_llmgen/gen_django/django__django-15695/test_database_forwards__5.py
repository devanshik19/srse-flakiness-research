import pytest
from django.db import models, transaction
from django.db.migrations.state import ModelState
from django.db.migrations.operations.models import CreateModel
from django.contrib.auth.models import User
from django.db import connection

@pytest.fixture
def create_model_operation():
    # Create an instance of CreateModel
    return CreateModel(
        name='CustomUser',
        fields=[('custom_field', models.CharField(max_length=100))],
        options={},
        bases=(User,),
        managers=[],
    )

def test_database_forwards(create_model_operation):
    app_label = 'auth'
    schema_editor = connection.schema_editor()
    
    # Prepare the state
    from_state = ModelState(app_label=app_label, model_name='user', fields={})
    to_state = ModelState(app_label=app_label, model_name='customuser', fields={'custom_field': models.CharField(max_length=100)})

    # Run the operation
    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)
    
    # Verify the model is created in the database
    assert 'customuser' in connection.introspection.table_names()
    
    # Check if the field exists
    with connection.schema_editor() as editor:
        model_class = editor.get_model(app_label, 'CustomUser')
        assert hasattr(model_class, 'custom_field')
    
    # Cleanup the created model
    schema_editor.remove_model(model_class)

def test_database_forwards_no_migrate(create_model_operation):
    app_label = 'auth'
    schema_editor = connection.schema_editor()
    
    # Simulate a scenario where the model should not be migrated
    def allow_migrate_model_mock(alias, model):
        return False
    create_model_operation.allow_migrate_model = allow_migrate_model_mock

    from_state = ModelState(app_label=app_label, model_name='user', fields={})
    to_state = ModelState(app_label=app_label, model_name='customuser', fields={'custom_field': models.CharField(max_length=100)})

    # Run the operation, expecting no exception
    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)
    
    # Verify the model is NOT created in the database
    assert 'customuser' not in connection.introspection.table_names()