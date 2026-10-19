import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.state import ProjectState
from django.db.migrations.operations.models import CreateModel

@pytest.fixture
def create_model_operation():
    return CreateModel(
        name='TestUserModel',
        fields=[
            ('username', models.CharField(max_length=150)),
            ('email', models.EmailField()),
        ],
        options={},
        bases=(User,),
        managers=[]
    )

def test_database_forwards(create_model_operation):
    app_label = 'auth'
    schema_editor = connections['default'].schema_editor()
    from_state = ProjectState()
    to_state = ProjectState()

    # Setting up the state to enable the operation
    to_state.create_model = create_model_operation

    # Execute the database_forwards method
    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

    # Check if the model was created successfully
    model = to_state.apps.get_model(app_label, 'TestUserModel')
    assert model is not None

    # Verify that we can create an instance of the newly created model
    user_instance = model.objects.create(username='testuser', email='test@example.com')
    assert user_instance.username == 'testuser'
    assert user_instance.email == 'test@example.com'

    # Clean up by removing the created model if needed
    schema_editor.remove_model(model)