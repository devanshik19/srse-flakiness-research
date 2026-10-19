import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def schema_editor(self):
        return BaseDatabaseSchemaEditor(connection, collect_sql=False)

    def test_alter_index_together_create(self, schema_editor):
        # Create the initial index_together setup
        User._meta.index_together = {('first_name', 'last_name')}
        schema_editor.alter_index_together(User, {('first_name', 'last_name')}, {('first_name', 'last_name'), ('email',)})

        # Check if the new index was created in the database
        indexes = connection.introspection.get_indexes(User._meta.db_table)
        assert ('first_name_email_idx' in indexes)

    def test_alter_index_together_delete(self, schema_editor):
        # Set up the index together
        User._meta.index_together = {('first_name', 'last_name')}
        schema_editor.alter_index_together(User, {('first_name', 'last_name')}, {('first_name',)})

        # Check if the old index is deleted
        indexes = connection.introspection.get_indexes(User._meta.db_table)
        assert ('first_name_last_name_idx' not in indexes)

    def test_alter_index_together_no_change(self, schema_editor):
        # Set the same index together
        User._meta.index_together = {('first_name', 'last_name')}
        schema_editor.alter_index_together(User, {('first_name', 'last_name')}, {('first_name', 'last_name')})

        # Ensure no new index is created
        indexes = connection.introspection.get_indexes(User._meta.db_table)
        assert len(indexes) == 1  # Only the original index should exist