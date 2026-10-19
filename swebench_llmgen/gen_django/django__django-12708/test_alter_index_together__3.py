import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class TestBaseDatabaseSchemaEditor:

    def setup_method(self):
        self.schema_editor = BaseDatabaseSchemaEditor(connection, collect_sql=False, atomic=True)

    def test_alter_index_together_add_index(self):
        # Prepare the initial state
        user_model = User
        old_index_together = [['username']]
        new_index_together = [['username'], ['email']]

        # Create the initial index
        self.schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

        # Assert the new index is created
        indexes = user_model._meta.indexes
        assert any(index.fields == ['username'] for index in indexes)
        assert any(index.fields == ['email'] for index in indexes)

    def test_alter_index_together_remove_index(self):
        # Prepare the initial state
        user_model = User
        old_index_together = [['username'], ['email']]
        new_index_together = [['username']]

        # Create the initial indexes
        self.schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

        # Assert that the 'email' index is removed
        indexes = user_model._meta.indexes
        assert any(index.fields == ['username'] for index in indexes)
        assert not any(index.fields == ['email'] for index in indexes)

    def test_alter_index_together_no_change(self):
        # Prepare the initial state
        user_model = User
        old_index_together = [['username']]
        new_index_together = [['username']]

        # Call with no changes
        self.schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

        # Assert the index remains unchanged
        indexes = user_model._meta.indexes
        assert len(indexes) == 1
        assert any(index.fields == ['username'] for index in indexes)

    def test_alter_index_together_multiple_changes(self):
        # Prepare the initial state
        user_model = User
        old_index_together = [['username'], ['email']]
        new_index_together = [['username'], ['email'], ['first_name']]

        # Create the new index
        self.schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

        # Assert all expected indexes are created
        indexes = user_model._meta.indexes
        assert any(index.fields == ['username'] for index in indexes)
        assert any(index.fields == ['email'] for index in indexes)
        assert any(index.fields == ['first_name'] for index in indexes)