import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.state import ProjectState
from django.db.migrations.operations.models import CreateModel

class TestCreateModel:
    
    @pytest.fixture
    def schema_editor(self):
        connection = connections['default']
        yield connection.schema_editor()

    @pytest.fixture
    def from_state(self):
        return ProjectState()

    @pytest.fixture
    def to_state(self):
        return ProjectState()

    def test_database_forwards_creates_model(self, schema_editor, from_state, to_state):
        # Arrange
        name = 'MyUser'
        fields = [('username', models.CharField(max_length=150))]
        options = {}
        bases = (User,)
        managers = []

        create_model_op = CreateModel(name, fields, options, bases, managers)

        # Set up the necessary data in to_state
        to_state.apps.get_model = lambda app_label, model_name: User if model_name == 'MyUser' else None
        to_state.apps.register_model('app_name', User)

        # Act
        create_model_op.database_forwards('app_name', schema_editor, from_state, to_state)

        # Assert
        assert 'myuser' in schema_editor.connection.introspection.table_names()
        
    def test_database_forwards_does_not_create_model_when_not_allowed(self, schema_editor, from_state, to_state):
        # Arrange
        name = 'MyUser'
        fields = [('username', models.CharField(max_length=150))]
        options = {}
        bases = (User,)
        managers = []

        create_model_op = CreateModel(name, fields, options, bases, managers)

        # Mock allow_migrate_model to return False
        create_model_op.allow_migrate_model = lambda alias, model: False

        # Set up the necessary data in to_state
        to_state.apps.get_model = lambda app_label, model_name: User if model_name == 'MyUser' else None
        to_state.apps.register_model('app_name', User)

        # Act
        create_model_op.database_forwards('app_name', schema_editor, from_state, to_state)

        # Assert
        assert 'myuser' not in schema_editor.connection.introspection.table_names()