import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def editor(self):
        return BaseDatabaseSchemaEditor(connection)

    def test_create_unique_sql_no_deferrable(self, editor):
        sql = editor._create_unique_sql(
            model=User,
            fields=[User._meta.get_field('username')],
            deferrable=False
        )
        assert sql is not None
        assert 'CREATE UNIQUE INDEX' in sql.sql

    def test_create_unique_sql_with_deferrable(self, editor):
        editor.connection.features.supports_deferrable_unique_constraints = True
        sql = editor._create_unique_sql(
            model=User,
            fields=[User._meta.get_field('username')],
            deferrable=True
        )
        assert sql is not None
        assert 'CREATE UNIQUE INDEX' in sql.sql

    def test_create_unique_sql_condition(self, editor):
        editor.connection.features.supports_partial_indexes = True
        sql = editor._create_unique_sql(
            model=User,
            fields=[User._meta.get_field('username')],
            condition="username IS NOT NULL"
        )
        assert sql is not None
        assert 'CREATE UNIQUE INDEX' in sql.sql

    def test_create_unique_sql_with_include(self, editor):
        editor.connection.features.supports_covering_indexes = True
        sql = editor._create_unique_sql(
            model=User,
            fields=[User._meta.get_field('username')],
            include=['email']
        )
        assert sql is not None
        assert 'CREATE UNIQUE INDEX' in sql.sql

    def test_create_unique_sql_with_expression(self, editor):
        editor.connection.features.supports_expression_indexes = True
        sql = editor._create_unique_sql(
            model=User,
            fields=[User._meta.get_field('username')],
            expressions=['LOWER(username)']
        )
        assert sql is not None
        assert 'CREATE UNIQUE INDEX' in sql.sql

    def test_create_unique_sql_not_supported(self, editor):
        editor.connection.features.supports_deferrable_unique_constraints = False
        sql = editor._create_unique_sql(
            model=User,
            fields=[User._meta.get_field('username')],
            deferrable=True
        )
        assert sql is None