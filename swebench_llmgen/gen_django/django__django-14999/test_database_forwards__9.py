import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.migrations.state import ProjectState
from django.db.migrations.operations.models import CreateModel

class TestCreateModel:
    
    @pytest.fixture
    def create_model_operation(self):
        return CreateModel('User', [], {})

    @pytest.fixture
    def app_label(self):
        return 'auth'
    
    @pytest.fixture
    def schema_editor(self):
        return connection.schema_editor()

    @pytest.fixture
    def from_state(self):
        return ProjectState()

    @pytest.fixture
    def to_state(self):
        return ProjectState()

    def test_database_forwards_creates_model(self, create_model_operation, app_label, schema_editor, from_state, to_state):
        # Setup initial state
        to_state.add_model(app_label, 'User', {
            'id': models.AutoField(primary_key=True),
            'username': models.CharField(max_length=150, unique=True),
            'password': models.CharField(max_length=128),
        })
        
        # Run database_forwards
        create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)
        
        # Assert the model has been created
        assert User in to_state.apps.get_models(app_label)
        
        # Check if the User model exists in the database
        assert connection.introspection.table_names() == ['auth_user']

    def test_database_forwards_without_migration(self, create_model_operation, app_label, schema_editor, from_state, to_state):
        # Setup initial state without allowing migration
        to_state.add_model(app_label, 'User', {
            'id': models.AutoField(primary_key=True),
            'username': models.CharField(max_length=150, unique=True),
            'password': models.CharField(max_length=128),
        })
        
        # Mocking method from the operation
        create_model_operation.allow_migrate_model = lambda alias, model: False
        
        # Run database_forwards
        create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)
        
        # Assert the model has not been created
        assert User not in to_state.apps.get_models(app_label)
        assert 'auth_user' not in connection.introspection.table_names()