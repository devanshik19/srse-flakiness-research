import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_delete_composed_index_valid(schema_editor):
    # Create a User model with a unique constraint on email
    User._meta.constraints.append(
        Index('idx_user_email', ['email'], unique=True)
    )

    # Set the sql for testing purpose
    sql = 'ALTER TABLE auth_user DROP INDEX idx_user_email;'

    # Run the method
    try:
        schema_editor._delete_composed_index(User, ['email'], {}, sql)
    except ValueError as e:
        pytest.fail(f"ValueError raised: {e}")

    # Verify that the index is deleted
    with connection.cursor() as cursor:
        cursor.execute("SHOW INDEX FROM auth_user WHERE Key_name = 'idx_user_email';")
        index_exists = cursor.fetchone() is not None
        assert not index_exists

def test_delete_composed_index_invalid_constraint_count(schema_editor):
    sql = 'ALTER TABLE auth_user DROP INDEX non_existent_index;'
    
    # Running with non-existent constraints should raise a ValueError
    with pytest.raises(ValueError, match="Found wrong number"):
        schema_editor._delete_composed_index(User, ['email'], {}, sql)

def test_delete_composed_index_more_than_one_constraint(schema_editor):
    # Adding a second unique constraint
    User._meta.constraints.append(
        Index('idx_user_email', ['email'], unique=True)
    )

    # Adding a second constraint with the same fields
    User._meta.constraints.append(
        Index('idx_user_email_duplicate', ['email'], unique=True)
    )

    sql = 'ALTER TABLE auth_user DROP INDEX idx_user_email;'

    # Expecting a ValueError since we have more than one constraint
    with pytest.raises(ValueError, match="Found wrong number"):
        schema_editor._delete_composed_index(User, ['email'], {}, sql)

    # Clean up the added constraints
    User._meta.constraints.pop()  # Remove duplicate constraint
    User._meta.constraints.pop()  # Remove the initial constraint