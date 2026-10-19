import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def schema_editor(self):
        return BaseDatabaseSchemaEditor(connection=connection, collect_sql=False, atomic=False)

    def test_create_unique_sql_no_conditions(self, schema_editor):
        model = User
        fields = [model._meta.get_field('username')]
        
        sql_statement = schema_editor._create_unique_sql(model, fields)
        
        assert sql_statement is not None
        assert 'UNIQUE' in str(sql_statement)

    def test_create_unique_sql_with_name(self, schema_editor):
        model = User
        fields = [model._meta.get_field('email')]
        name = "unique_email_constraint"
        
        sql_statement = schema_editor._create_unique_sql(model, fields, name=name)
        
        assert sql_statement is not None
        assert sql_statement.name == schema_editor.quote_name(name)

    def test_create_unique_sql_with_condition(self, schema_editor):
        model = User
        fields = [model._meta.get_field('username')]
        condition = 'username IS NOT NULL'
        
        sql_statement = schema_editor._create_unique_sql(model, fields, condition=condition)
        
        assert sql_statement is not None
        assert sql_statement.condition == schema_editor._index_condition_sql(condition)

    def test_create_unique_sql_with_deferrable(self, schema_editor):
        model = User
        fields = [model._meta.get_field('username')]
        deferrable = True
        
        # Assuming the feature supports deferrable constraints is set to True in the connection's features.
        schema_editor.connection.features.supports_deferrable_unique_constraints = True
        
        sql_statement = schema_editor._create_unique_sql(model, fields, deferrable=deferrable)
        
        assert sql_statement is not None
        assert sql_statement.deferrable is not None

    def test_create_unique_sql_with_include(self, schema_editor):
        model = User
        fields = [model._meta.get_field('username')]
        include = ['first_name', 'last_name']
        
        # Assuming the feature supports covering indexes is set to True in the connection's features.
        schema_editor.connection.features.supports_covering_indexes = True
        
        sql_statement = schema_editor._create_unique_sql(model, fields, include=include)
        
        assert sql_statement is not None
        assert sql_statement.include == schema_editor._index_include_sql(model, include)

    def test_create_unique_sql_with_expressions(self, schema_editor):
        model = User
        fields = [model._meta.get_field('username')]
        expressions = ['LOWER(username)']
        
        # Assuming the feature supports expression indexes is set to True in the connection's features.
        schema_editor.connection.features.supports_expression_indexes = True
        
        sql_statement = schema_editor._create_unique_sql(model, fields, expressions=expressions)
        
        assert sql_statement is not None
        assert sql_statement.columns == schema_editor._index_columns(model._meta.db_table, expressions)

    def test_create_unique_sql_with_incompatible_features(self, schema_editor):
        model = User
        fields = [model._meta.get_field('username')]
        
        # Set features to not support deferrable unique constraints
        schema_editor.connection.features.supports_deferrable_unique_constraints = False
        schema_editor.connection.features.supports_partial_indexes = False
        schema_editor.connection.features.supports_covering_indexes = False
        schema_editor.connection.features.supports_expression_indexes = False
        
        sql_statement = schema_editor._create_unique_sql(model, fields, deferrable=True, condition='username IS NOT NULL')

        assert sql_statement is None