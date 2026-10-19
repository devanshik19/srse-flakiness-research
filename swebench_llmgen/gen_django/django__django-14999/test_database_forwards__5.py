import pytest
from django.db import migrations, models
from django.contrib.auth.models import User
from django.db.migrations import Migration
from django.db.migrations.state import ProjectState
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.operations.models import CreateModel

@pytest.fixture
def create_model_operation():
    return CreateModel("MyModel", [("name", models.CharField(max_length=100))], {}, (), [])

@pytest.fixture
def migration_executor():
    return MigrationExecutor(Migration("my_app", "0001_initial"))

def test_database_forwards_success(create_model_operation, migration_executor):
    app_label = "my_app"
    schema_editor = migration_executor.connection.schema_editor()
    from_state = ProjectState()
    to_state = from_state.clone()
    to_state.apps.register_models(app_label, [User])  # Ensure User is registered in the state

    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

    assert migration_executor.connection.introspection.table_names() == {'auth_user', 'my_app_mymodel'}

def test_database_forwards_skip(create_model_operation, migration_executor):
    app_label = "my_app"
    schema_editor = migration_executor.connection.schema_editor()
    from_state = ProjectState()
    to_state = from_state.clone()
    to_state.apps.register_models(app_label, [User])  # Ensure User is registered in the state

    # Mock allow_migrate_model to return False
    original_allow_migrate_model = create_model_operation.allow_migrate_model
    create_model_operation.allow_migrate_model = lambda alias, model: False

    create_model_operation.database_forwards(app_label, schema_editor, from_state, to_state)

    assert 'my_app_mymodel' not in migration_executor.connection.introspection.table_names()

    # Restore original method
    create_model_operation.allow_migrate_model = original_allow_migrate_model