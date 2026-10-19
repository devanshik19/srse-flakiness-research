import pytest
from django.db importconnection
from django.contrib.auth.models import User
from django.db.migrations.operations.models import CreateModel
from django.db.migrations.state import ProjectState
from django.db.migrations.schema import SchemaEditor

@pytest.fixture
def create_model_operation():
    return CreateModel(
        name='TestModel',
        fields=[('field_1', models.CharField(max_length=100))],
        options={},
        bases=(models.Model,),
        managers=[]
    )

def test_database_forwards(create_model_operation):
    app_label = 'auth'
    schema_editor = SchemaEditor(connection)
    from_state = ProjectState()
    to_state = ProjectState()
    
    # Add model to `to_state`
    to_state.apps.register_model(app_label, User)

    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

    # Check if the model was created
    assert 'auth_testmodel' in connection.introspection.table_names()
    assert len(User.objects.all()) == 0  # Ensure that the User model still works