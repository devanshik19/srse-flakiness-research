import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_alter_unique_together(schema_editor):
    # Setup initial state
    User._meta.unique_together = {('username', 'email')}
    old_unique_together = {('username', 'email')}
    new_unique_together = {('username',)}

    # Test removing a unique constraint
    schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)
    
    # Execute SQL to verify unique constraint removal
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT count(*) FROM information_schema.table_constraints "
            "WHERE table_name='auth_user' "
            "AND constraint_type='UNIQUE' "
            "AND constraint_name LIKE '%username_email%'"
        )
        assert cursor.fetchone()[0] == 0

    # Test adding a unique constraint
    old_unique_together = {('username',)}
    new_unique_together = {('username', 'email')}
    
    schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)

    # Execute SQL to verify unique constraint addition
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT count(*) FROM information_schema.table_constraints "
            "WHERE table_name='auth_user' "
            "AND constraint_type='UNIQUE' "
            "AND constraint_name LIKE '%username_email%'"
        )
        assert cursor.fetchone()[0] == 1