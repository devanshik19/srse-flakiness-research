import pytest
from django.db import migrations, models
from django.contrib.auth import get_user_model

from django.db.migrations.operations.models import CreateModel

User = get_user_model()

@pytest.fixture
def create_model_operation():
    return CreateModel("MyModel", [("name", models.CharField(max_length=100))], {}, (), ())

@pytest.mark.parametrize("allow_migrate", [True, False])
def test_database_forwards(create_model_operation, allow_migrate, schema_editor):
    # Simulate the behavior of allow_migrate_model
    def mock_allow_migrate_model(alias, model):
        return allow_migrate

    create_model_operation.allow_migrate_model = mock_allow_migrate_model
    
    # Prepare from_state and to_state
    from_state = migrations.state.State()
    to_state = migrations.state.State()
    to_state.apps.register_model("myapp", User)
    
    # Run the database_forwards method
    create_model_operation.database_forwards("myapp", schema_editor, from_state, to_state)

    if allow_migrate:
        assert schema_editor.has_model("myapp", "MyModel")
    else:
        assert not schema_editor.has_model("myapp", "MyModel")