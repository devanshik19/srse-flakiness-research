import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def schema_editor(self):
        return BaseDatabaseSchemaEditor(connection=connection, collect_sql=False, atomic=False)

    def test_delete_composed_index_success(self, schema_editor):
        # Arrange: create a user and an index
        user = User(username='testuser', password='password')
        user.save()

        model = User
        fields = ['username']
        constraint_kwargs = {}
        sql = 'DELETE INDEX sql_delete_test_index'

        schema_editor.add_index(model, schema_editor._create_index_sql(model))

        # Act: call the focal method
        schema_editor._delete_composed_index(model, fields, constraint_kwargs, sql)

        # Assert: ensure the index is deleted
        assert not any(index.name == 'sql_delete_test_index' for index in model._meta.indexes)

    def test_delete_composed_index_value_error(self, schema_editor):
        model = User
        fields = ['username']
        constraint_kwargs = {}
        sql = 'DELETE INDEX sql_delete_invalid_index'

        # Act & Assert: should raise ValueError when constraints are not found
        with pytest.raises(ValueError) as excinfo:
            schema_editor._delete_composed_index(model, fields, constraint_kwargs, sql)
        
        assert "Found wrong number" in str(excinfo.value)