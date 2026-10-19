import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db import connection

@pytest.mark.django_db
def test_alter_field_rename():
    editor = DatabaseSchemaEditor()

    # Set up a model for testing
    old_field = User._meta.get_field('username')
    new_field = User._meta.get_field('email')
    
    # Modify the field's column name
    new_field.column = 'new_username'
    
    # Create a new column SQL
    editor.column_sql = lambda model, field: f'"{field.column}"'
    
    # Execute the _alter_field method to rename the column
    editor._alter_field(
        model=User,
        old_field=old_field,
        new_field=new_field,
        old_type=old_field.get_internal_type(),
        new_type=new_field.get_internal_type(),
        old_db_params={},
        new_db_params={},
        strict=False
    )

    # Assert that the column has been renamed in the database
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(auth_user)")
    columns = [row[1] for row in cursor.fetchall()]
    assert 'new_username' in columns
    assert 'username' not in columns

def test_alter_field_rebuild_table():
    editor = DatabaseSchemaEditor()
    
    # Create a new field for testing
    old_field = User._meta.get_field('username')
    new_field = models.Field()
    new_field.column = 'username'
    new_field.db_constraint = False  # Simulating no constraints
    
    # Define the internal types for comparison
    old_type = old_field.get_internal_type()
    new_type = old_field.get_internal_type()

    # Execute the _alter_field method to rebuild the table
    editor._alter_field(
        model=User,
        old_field=old_field,
        new_field=new_field,
        old_type=old_type,
        new_type=new_type,
        old_db_params={},
        new_db_params={},
        strict=False
    )

    # Check if the table should be rebuilt (for internal testing purposes)
    assert editor.connection.features.can_alter_table_rename_column is False  # Enforce table recreation

    # Further assertions can be added based on the expected behavior of `_remake_table`
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
    assert cursor.fetchone() is not None