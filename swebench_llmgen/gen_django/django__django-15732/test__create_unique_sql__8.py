import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture()
    def editor(self):
        return BaseDatabaseSchemaEditor(connection, collect_sql=False)

    def test_create_unique_sql_with_deferrable(self, editor):
        # Test with deferrable set to True, assuming supports_deferrable_unique_constraints is true
        editor.connection.features.supports_deferrable_unique_constraints = True
        sql_statement = editor._create_unique_sql(User, [User._meta.get_field('username')], deferrable=True)
        assert sql_statement is not None
        assert "UNIQUE" in str(sql_statement)

    def test_create_unique_sql_without_deferrable(self, editor):
        # Test without deferrable, still should create unique
        editor.connection.features.supports_deferrable_unique_constraints = True
        sql_statement = editor._create_unique_sql(User, [User._meta.get_field('email')])
        assert sql_statement is not None
        assert "UNIQUE" in str(sql_statement)

    def test_create_unique_sql_with_condition(self, editor):
        # Test with condition where support for partial indexes is required
        editor.connection.features.supports_partial_indexes = True
        sql_statement = editor._create_unique_sql(User, [User._meta.get_field('username')], condition="username IS NOT NULL")
        assert sql_statement is not None

    def test_create_unique_sql_with_non_supported_condition(self, editor):
        editor.connection.features.supports_partial_indexes = False
        sql_statement = editor._create_unique_sql(User, [User._meta.get_field('username')], condition="username IS NOT NULL")
        assert sql_statement is None

    def test_create_unique_sql_with_include(self, editor):
        # Test with include, ensuring covering index is supported
        editor.connection.features.supports_covering_indexes = True
        sql_statement = editor._create_unique_sql(User, [User._meta.get_field('username')], include=['date_joined'])
        assert sql_statement is not None

    def test_create_unique_sql_with_not_supported_include(self, editor):
        editor.connection.features.supports_covering_indexes = False
        sql_statement = editor._create_unique_sql(User, [User._meta.get_field('username')], include=['date_joined'])
        assert sql_statement is None

    def test_create_unique_sql_with_expressions(self, editor):
        # Test with expressions where support for expression indexes is granted
        editor.connection.features.supports_expression_indexes = True
        sql_statement = editor._create_unique_sql(User, [User._meta.get_field('username')], expressions=['LOWER(username)'])
        assert sql_statement is not None

    def test_create_unique_sql_with_not_supported_expressions(self, editor):
        editor.connection.features.supports_expression_indexes = False
        sql_statement = editor._create_unique_sql(User, [User._meta.get_field('username')], expressions=['LOWER(username)'])
        assert sql_statement is None

    def test_create_unique_sql_no_columns(self, editor):
        sql_statement = editor._create_unique_sql(User, [], name='unique_name')
        assert sql_statement is None