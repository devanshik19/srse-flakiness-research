import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.mark.parametrize(
    "constraint_kwargs, expected_error, expected_constraint_count",
    [
        ({}, ValueError, 0),  # Expect ValueError for no constraints found
        ({'unique': True}, ValueError, 0),  # Unique constraint query returns incorrect count
        ({}, None, 1),  # Valid case: exactly one constraint found
    ]
)
def test_delete_composed_index(constraint_kwargs, expected_error, expected_constraint_count):
    # Prepare the database schema editor
    schema_editor = BaseDatabaseSchemaEditor(connection)

    # Create a user model instance to use for testing
    user_model = User.objects.create(username='testuser', password='password123')

    # Manually create a composed index for the test
    # Assuming the composed index normally would be added via migrations
    # Here we would normally check for existing index/constraints after alterations

    # Function to simulate adding a composed index
    def add_composed_index(model, fields):
        index_name = f"{model._meta.db_table}_{'_'.join(fields)}_idx"
        schema_editor.execute(schema_editor._create_index_sql(model, fields, name=index_name))

    fields = ['username']  # Adjust fields according to actual constraints in User model
    add_composed_index(User, fields)

    # Now test `_delete_composed_index`
    sql = "DELETE INDEX"  # Placeholder for the expected SQL structure

    if expected_error:
        with pytest.raises(expected_error):
            schema_editor._delete_composed_index(User, fields, constraint_kwargs, sql)
    else:
        schema_editor._delete_composed_index(User, fields, constraint_kwargs, sql)
        # Verify if the index was actually deleted
        assert len(schema_editor._constraint_names(User, fields)) == expected_constraint_count