import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def schema_editor(self):
        return BaseDatabaseSchemaEditor(connection)

    def test_alter_index_together_create_index(self, schema_editor):
        # Arrange
        user_model = User
        old_index_together = [['username']]
        new_index_together = [['username'], ['email']]

        # Act
        schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

        # Assert that the index "_idx" for email column is created
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pg_indexes WHERE tablename = 'auth_user' AND indexname = 'auth_user_email_idx'")
            assert cursor.fetchone() is not None

    def test_alter_index_together_delete_index(self, schema_editor):
        # Arrange
        user_model = User
        old_index_together = [['username'], ['email']]
        new_index_together = [['username']]

        # Act
        schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

        # Assert that the index "_idx" for email column is deleted
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pg_indexes WHERE tablename = 'auth_user' AND indexname = 'auth_user_email_idx'")
            assert cursor.fetchone() is None

    def test_alter_index_together_no_change(self, schema_editor):
        # Arrange
        user_model = User
        old_index_together = [['username']]
        new_index_together = [['username']]

        # Act
        schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

        # Assert that no changes have been made (no errors raised)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pg_indexes WHERE tablename = 'auth_user'")
            assert len(cursor.fetchall()) == 0  # Assumes no indexes are created by default