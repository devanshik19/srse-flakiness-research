import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

def test_delete_composed_index():
    # Set up the schema editor
    editor = BaseDatabaseSchemaEditor(connection)

    # Create a model instance and add an index
    user = User.objects.create(username="testuser", email="test@example.com")
    user.save()

    # Define fields and constraints
    fields = ['username']
    constraint_kwargs = {}
    
    # Add a unique index on the username field to simulate the test case
    editor.add_index(User, editor.create_index_sql(User, fields, unique=True))

    # Execute the _delete_composed_index function
    sql = "DROP INDEX IF EXISTS auth_user_username_un"
    
    # Get the created constraint names
    constraint_names = editor._constraint_names(User, ['username'])

    # Ensure one constraint exists
    assert len(constraint_names) == 1

    # Now delete the index using the _delete_composed_index function
    editor._delete_composed_index(User, fields, constraint_kwargs, sql)

    # Check if the index was successfully removed
    with pytest.raises(ValueError) as excinfo:
        editor._delete_composed_index(User, fields, constraint_kwargs, sql)

    assert "Found wrong number" in str(excinfo.value)