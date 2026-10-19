import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.core.management.color import no_style

class TestBaseDatabaseOperations:
    
    def test_sql_flush_with_reset_sequences(self):
        # Create a user instance
        User.objects.create(username='testuser1')

        # Get the BaseDatabaseOperations instance
        operations = connection.ops

        # Retrieve the SQL commands for flushing the database
        sql_commands = operations.sql_flush(style=no_style(), tables=['auth_user'], reset_sequences=True)

        # Check that the correct SQL commands are generated
        expected_sql = [
            'TRUNCATE TABLE "auth_user" CASCADE;',
            'ALTER SEQUENCE "auth_user_id_seq" RESTART WITH 1;'
        ]
        
        assert sql_commands == expected_sql

    def test_sql_flush_without_reset_sequences(self):
        # Create a user instance
        User.objects.create(username='testuser2')

        # Get the BaseDatabaseOperations instance
        operations = connection.ops

        # Retrieve the SQL commands for flushing the database without resetting sequences
        sql_commands = operations.sql_flush(style=no_style(), tables=['auth_user'], reset_sequences=False)

        # Check that the correct SQL commands are generated
        expected_sql = [
            'TRUNCATE TABLE "auth_user" CASCADE;'
        ]
        
        assert sql_commands == expected_sql

    def test_sql_flush_with_allow_cascade(self):
        # Create a user instance
        User.objects.create(username='testuser3')

        # Get the BaseDatabaseOperations instance
        operations = connection.ops

        # Retrieve the SQL commands for flushing the database with allow_cascade
        sql_commands = operations.sql_flush(style=no_style(), tables=['auth_user'], reset_sequences=True, allow_cascade=True)

        # Ensure CASCADE behavior is respected
        expected_sql = [
            'TRUNCATE TABLE "auth_user" CASCADE;',
            'ALTER SEQUENCE "auth_user_id_seq" RESTART WITH 1;'
        ]
        
        assert sql_commands == expected_sql