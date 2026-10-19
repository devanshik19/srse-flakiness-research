import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestAlterUniqueTogether:

    @pytest.fixture
    def schema_editor(self):
        return BaseDatabaseSchemaEditor(connection)

    def test_alter_unique_together_add(self, schema_editor):
        User._meta.unique_together = {('username',)}
        old_unique_together = {('username',)}
        new_unique_together = {('username',), ('email',)}

        schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)

        # Check if the unique constraint for email has been added
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public' AND tablename = 'auth_user' AND indexname = 'auth_user_email_unique';")
            count = cursor.fetchone()[0]
            assert count == 1

    def test_alter_unique_together_remove(self, schema_editor):
        User._meta.unique_together = {('username',), ('email',)}
        old_unique_together = {('username',), ('email',)}
        new_unique_together = {('username',)}

        schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)

        # Check if the unique constraint for email has been removed
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public' AND tablename = 'auth_user' AND indexname = 'auth_user_email_unique';")
            count = cursor.fetchone()[0]
            assert count == 0

    def test_alter_unique_together_no_change(self, schema_editor):
        User._meta.unique_together = {('username',)}
        old_unique_together = {('username',)}
        new_unique_together = {('username',)}

        schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)

        # Check that the unique constraint is unchanged
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public' AND tablename = 'auth_user' AND indexname = 'auth_user_username_unique';")
            count = cursor.fetchone()[0]
            assert count == 1