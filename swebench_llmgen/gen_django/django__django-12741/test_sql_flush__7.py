import pytest
from django.core.management.color import no_style
from django.contrib.auth.models import User
from django.db import connections

class TestBaseDatabaseOperations:

    def test_sql_flush_without_reset_sequences(self):
        # Arrange
        db_alias = 'default'
        cursor = connections[db_alias].cursor()
        operations = connections[db_alias].operations

        # Create a user to have data in the database
        User.objects.create(username='testuser', password='password')

        # Act
        sql_statements = operations.sql_flush(no_style(), ['auth_user'], reset_sequences=False)

        # Assert
        assert isinstance(sql_statements, list)
        assert len(sql_statements) > 0
        assert 'DELETE FROM "auth_user"' in sql_statements

    def test_sql_flush_with_reset_sequences(self):
        # Arrange
        db_alias = 'default'
        cursor = connections[db_alias].cursor()
        operations = connections[db_alias].operations
        
        # Create a user to have data in the database
        User.objects.create(username='testuser', password='password')

        # Act
        sql_statements = operations.sql_flush(no_style(), ['auth_user'], reset_sequences=True)

        # Assert
        assert isinstance(sql_statements, list)
        assert len(sql_statements) > 0
        assert 'DELETE FROM "auth_user"' in sql_statements
        assert 'ALTER SEQUENCE "auth_user_id_seq" RESTART WITH' in sql_statements

    def test_sql_flush_with_allow_cascade(self):
        # Arrange
        db_alias = 'default'
        cursor = connections[db_alias].cursor()
        operations = connections[db_alias].operations
        
        # Create a user to have data in the database
        User.objects.create(username='testuser', password='password')

        # Act
        sql_statements = operations.sql_flush(no_style(), ['auth_user'], allow_cascade=True)

        # Assert
        assert isinstance(sql_statements, list)
        assert len(sql_statements) > 0
        assert 'DELETE FROM "auth_user"' in sql_statements