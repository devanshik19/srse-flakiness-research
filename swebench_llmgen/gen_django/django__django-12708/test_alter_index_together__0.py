import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class CustomSchemaEditor(BaseDatabaseSchemaEditor):
    def _delete_composed_index(self, model, fields, constraint_kwargs, sql):
        # This is a minimal implementation for the test.
        index_name = self._create_index_name(model._meta.db_table, fields)
        self.execute(sql.format(index=index_name))

    def _create_index_sql(self, model, fields, suffix):
        index_name = self._create_index_name(model._meta.db_table, [f.column for f in fields], suffix)
        return "CREATE INDEX {index} ON {table} ({columns});".format(
            index=index_name,
            table=self.quote_name(model._meta.db_table),
            columns=', '.join([self.quote_name(f.column) for f in fields]),
        )

@pytest.fixture
def schema_editor():
    return CustomSchemaEditor(connection)

def test_alter_index_together(schema_editor):
    # Set up the initial state with index_together
    user_model = User
    old_index_together = [['username']]
    new_index_together = [['username', 'email']]

    # Create old index
    schema_editor.alter_index_together(user_model, old_index_together, [])
    
    # Ensure the index is created
    indexes = connection.introspection.get_indexes(user_model._meta.db_table)
    assert 'username_idx' in indexes

    # Call the focal function to alter the index together
    schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

    # Ensure the old index is deleted and the new index is created
    indexes = connection.introspection.get_indexes(user_model._meta.db_table)
    assert 'username_idx' not in indexes
    assert 'username_email_idx' in indexes

    # Clean up - revert to previous state
    schema_editor.alter_index_together(user_model, new_index_together, old_index_together)