import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class TestDatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    def __init__(self, connection, collect_sql=False, atomic=False):
        super().__init__(connection, collect_sql, atomic)

    def execute(self, sql, params=None):
        # Overriding execute method for testing purposes
        return sql


def test_delete_composed_index_valid_constraint():
    editor = TestDatabaseSchemaEditor(connection=None)
    user_model = User
    user_model._meta.constraints = []
    
    # Create a unique constraint on the 'username' field
    user_model._meta.indexes = [
        models.Index(fields=['username'], name='unique_username')
    ]

    # Simulate a proper SQL for deleting an index
    sql = "DROP INDEX unique_username"

    # Call the method with valid parameters
    editor._delete_composed_index(user_model, ['username'], {}, sql)

    # If no exceptions were raised, the test should pass.


def test_delete_composed_index_invalid_constraint():
    editor = TestDatabaseSchemaEditor(connection=None)
    user_model = User
    user_model._meta.constraints = []
    
    # Create a unique constraint on the 'username' field
    user_model._meta.indexes = [
        models.Index(fields=['username'], name='unique_username')
    ]

    # Simulate a SQL for deleting an index
    sql = "DROP INDEX unique_username"

    # Test for ValueError when there are no matching constraints
    with pytest.raises(ValueError):
        editor._delete_composed_index(user_model, ['non_existing_field'], {}, sql)


def test_delete_composed_index_multiple_constraints():
    editor = TestDatabaseSchemaEditor(connection=None)
    user_model = User
    
    # Simulate multiple indexes
    user_model._meta.constraints = []
    user_model._meta.indexes = [
        models.Index(fields=['username'], name='unique_username'),
        models.Index(fields=['username'], name='another_index'),
    ]

    sql = "DROP INDEX unique_username"

    # Test for ValueError when more than one constraint is found
    with pytest.raises(ValueError):
        editor._delete_composed_index(user_model, ['username'], {}, sql)