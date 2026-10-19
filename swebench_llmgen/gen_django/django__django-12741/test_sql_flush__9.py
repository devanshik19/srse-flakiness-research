import pytest
from django.contrib.auth.models import User
from django.db.backends.base.operations import BaseDatabaseOperations

class CustomDatabaseOperations(BaseDatabaseOperations):
    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        # Here we would typically implement the actual SQL flush for the database.
        # For testing purposes, this implementation just returns mock SQL statements.
        sql_statements = []
        for table in tables:
            sql_statements.append(f'TRUNCATE TABLE {table};')
            if reset_sequences:
                sql_statements.append(f'SELECT SETVAL(pg_get_serial_sequence("{table}", "id"), 1, false);')
        return sql_statements

@pytest.mark.django_db
def test_sql_flush():
    # Arrange
    operations = CustomDatabaseOperations(None)
    User.objects.create(username='testuser1')
    User.objects.create(username='testuser2')
    
    # Act
    result = operations.sql_flush(None, ['auth_user'], reset_sequences=True)

    # Assert
    assert result == [
        'TRUNCATE TABLE auth_user;',
        'SELECT SETVAL(pg_get_serial_sequence("auth_user", "id"), 1, false);'
    ]
    # Ensure the database is flushed
    assert User.objects.count() == 0