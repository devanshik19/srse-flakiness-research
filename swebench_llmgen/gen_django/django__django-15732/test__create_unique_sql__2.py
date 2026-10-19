import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class TestBaseDatabaseSchemaEditor:
    def setup_method(self):
        self.connection = connections['default']
        self.schema_editor = BaseDatabaseSchemaEditor(self.connection, collect_sql=False, atomic=True)

    def test_create_unique_sql_no_deferrable_support(self):
        self.connection.features.supports_deferrable_unique_constraints = False
        sql_statement = self.schema_editor._create_unique_sql(User, [User._meta.get_field('username')])
        assert sql_statement is None

    def test_create_unique_sql_no_partial_index_support(self):
        self.connection.features.supports_partial_indexes = False
        sql_statement = self.schema_editor._create_unique_sql(User, [User._meta.get_field('username')], condition='username IS NOT NULL')
        assert sql_statement is None

    def test_create_unique_sql_no_covering_index_support(self):
        self.connection.features.supports_covering_indexes = False
        sql_statement = self.schema_editor._create_unique_sql(User, [User._meta.get_field('username')], include=['email'])
        assert sql_statement is None

    def test_create_unique_sql_no_expression_index_support(self):
        self.connection.features.supports_expression_indexes = False
        sql_statement = self.schema_editor._create_unique_sql(User, [User._meta.get_field('username')], expressions=['UPPER(username)'])
        assert sql_statement is None

    def test_create_unique_sql_with_conditions(self):
        sql_statement = self.schema_editor._create_unique_sql(
            User,
            [User._meta.get_field('username')],
            condition='username IS NOT NULL',
            deferrable=True
        )
        assert sql_statement is not None
        assert sql_statement.sql == self.schema_editor.sql_create_unique_index

    def test_create_unique_sql_with_custom_name(self):
        sql_statement = self.schema_editor._create_unique_sql(
            User,
            [User._meta.get_field('username')],
            name='unique_username'
        )
        assert sql_statement is not None
        assert sql_statement.name == 'unique_username'

    def test_create_unique_sql_with_missing_fields(self):
        sql_statement = self.schema_editor._create_unique_sql(
            User,
            [],
        )
        assert sql_statement is not None
        assert sql_statement.columns is not None