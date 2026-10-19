import pytest
from django.contrib.auth.models import User
from django.core.management.color import no_style
from django.db import connection
from django.db.backends.base.operations import BaseDatabaseOperations

class TestBaseDatabaseOperations(BaseDatabaseOperations):
    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        return super().sql_flush(style, tables, reset_sequences=reset_sequences, allow_cascade=allow_cascade)

def test_sql_flush_resets_sequences():
    operations = TestBaseDatabaseOperations(connection)

    # Create test data
    User.objects.create(username='testuser1')
    User.objects.create(username='testuser2')

    # Ensure users are created
    assert User.objects.count() == 2

    # Flush the database tables
    sql_statements = operations.sql_flush(no_style(), [User._meta.db_table], reset_sequences=True)

    # Check the expected SQL statements
    assert "DELETE FROM" in sql_statements[0]  # A delete statement should be present
    assert "ALTER SEQUENCE" in sql_statements[1]  # A sequence reset should be present for the User model

    # Execute the SQL statements
    with connection.cursor() as cursor:
        for statement in sql_statements:
            cursor.execute(statement)

    # Verify that users have been removed
    assert User.objects.count() == 0

def test_sql_flush_allows_cascade():
    operations = TestBaseDatabaseOperations(connection)

    # Create test data
    User.objects.create(username='testuser1')
    User.objects.create(username='testuser2')

    # Ensure users are created
    assert User.objects.count() == 2

    # Flush the database tables with cascade
    sql_statements = operations.sql_flush(no_style(), [User._meta.db_table], reset_sequences=True, allow_cascade=True)

    assert len(sql_statements) > 0  # Expect some SQL statements to be returned

    # Execute the SQL statements
    with connection.cursor() as cursor:
        for statement in sql_statements:
            cursor.execute(statement)

    # Verify users are removed
    assert User.objects.count() == 0