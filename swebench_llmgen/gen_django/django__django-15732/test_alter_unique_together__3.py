import pytest
from django.contrib.auth.models import User
from django.db import connections

@pytest.fixture
def schema_editor():
    connection = connections['default']
    return connection.schema_editor()

def test_alter_unique_together(schema_editor):
    user_model = User
    # Set up initial unique_together constraint
    old_unique_together = [['username', 'email']]
    new_unique_together = [['username', 'email'], ['first_name', 'last_name']]

    # Apply the old unique_together
    schema_editor.alter_unique_together(user_model, [], old_unique_together)

    # Verify that the unique_together constraint is in place
    assert schema_editor._constraint_names(user_model, ['username', 'email'], unique=True)

    # Alter the unique_together to new value
    schema_editor.alter_unique_together(user_model, old_unique_together, new_unique_together)

    # Check that the old unique_together has been deleted
    assert not schema_editor._constraint_names(user_model, ['username', 'email'], unique=True)

    # Check that the new unique_together has been created
    assert schema_editor._constraint_names(user_model, ['first_name', 'last_name'], unique=True)