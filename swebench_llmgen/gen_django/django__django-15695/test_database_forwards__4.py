import pytest
from django.db import migrations, models
from django.contrib.auth.models import User
from django.db.migrations.state import ProjectState
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestCreateModel:
    
    @pytest.fixture
    def create_model_op(self):
        class CreateModel(migrations.CreateModel):
            def __init__(self, name, fields=None, options=None, bases=None, managers=None):
                super().__init__(name, fields, options, bases, managers)
            
            def allow_migrate_model(self, alias, model):
                return True  # Allow migration for all models

        return CreateModel(name='TestModel', fields={'name': models.CharField(max_length=255)}, options={}, bases=(models.Model,))

    @pytest.fixture
    def schema_editor(self):
        class MockSchemaEditor(BaseDatabaseSchemaEditor):
            def create_model(self, model):
                assert model._meta.model_name == 'testmodel'
                
        return MockSchemaEditor()

    def test_database_forwards_creates_model(self, create_model_op, schema_editor):
        from_state = ProjectState()
        to_state = ProjectState()
        to_state.apps = migrations.state.Apps({"testapp": create_model_op})

        create_model_op.database_forwards('testapp', schema_editor, from_state, to_state)

    def test_database_forwards_allows_migrate_model(self, create_model_op, schema_editor):
        model = User  # Using an existing model to verify
        assert create_model_op.allow_migrate_model(schema_editor.connection.alias, model)