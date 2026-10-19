import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.core.management.color import no_style

class TestBaseDatabaseOperations:

    def test_sql_flush_reset_sequences(self):
        # Create some users to flush
        User.objects.create(username='user1')
        User.objects.create(username='user2')

        # Get database connection and operations
        connection = connections['default']
        operations = connection.ops
        
        # Generate the SQL statements for flushing
        sql_statements = operations.sql_flush(no_style(), [User._meta.db_table], reset_sequences=True)

        # Check if the SQL statements include TRUNCATE and sequences reset
        assert any("TRUNCATE" in sql for sql in sql_statements)
        assert any("ALTER SEQUENCE" in sql for sql in sql_statements)

    def test_sql_flush_allow_cascade(self):
        # Create some users to flush
        User.objects.create(username='user1')
        User.objects.create(username='user2')

        connection = connections['default']
        operations = connection.ops

        # Generate the SQL statements for flushing with allow_cascade
        sql_statements = operations.sql_flush(no_style(), [User._meta.db_table], allow_cascade=True)

        # Check that the generated SQL includes CASCADE (this assumes that the underlying DB recognizes it)
        assert any("CASCADE" in sql for sql in sql_statements)

    def test_sql_flush_without_reset_sequences(self):
        # Create some users to flush
        User.objects.create(username='user1')
        User.objects.create(username='user2')

        connection = connections['default']
        operations = connection.ops

        # Generate the SQL statements for flushing without reset_sequences
        sql_statements = operations.sql_flush(no_style(), [User._meta.db_table], reset_sequences=False)

        # Check if the SQL statements still include TRUNCATE
        assert any("TRUNCATE" in sql for sql in sql_statements)
        assert not any("ALTER SEQUENCE" in sql for sql in sql_statements)