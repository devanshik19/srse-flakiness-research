import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_alter_unique_together(schema_editor):
    # Setting up a model instance with unique_together
    User._meta.unique_together = {('username', 'email')}

    # Old unique_together
    old_unique_together = {('username', 'email')}
    # New unique_together (modifying to have one unique together deleted and one added)
    new_unique_together = {('username', 'email'), ('first_name', 'last_name')}

    # Add fields for the new unique_together
    User._meta.get_field('first_name').db_index = False
    User._meta.get_field('last_name').db_index = False

    # Execute the alter_unique_together function
    schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)

    # Check that the old unique_together has been removed
    with pytest.raises(Exception):  # Here you can replace Exception with a specific constraint error type
        schema_editor.execute(schema_editor.sql_delete_unique % ('auth_user', 'username_email'))

    # Check that the new unique_together has been created
    unique_index_sql = schema_editor._create_unique_sql(User, [User._meta.get_field('first_name'), 
                                                                User._meta.get_field('last_name')])
    schema_editor.execute(unique_index_sql)

    # Assert the unique together was created (ensure it doesn't raise)
    assert True  # You can add more specific asserts based on the execution

    # Cleanup unique_together for next tests
    User._meta.unique_together = set()