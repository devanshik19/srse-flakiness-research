import pytest
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode
from django.db.models.fields.related_lookups import RelatedIn
from django.db.models.sql.compiler import SQLCompiler
from django.db.backends.base.base import BaseDatabaseWrapper

@pytest.fixture
def setup_related_lookup():
    # Initiate a mock for lhs (left-hand side) and create a RelatedIn instance
    class MockMultiColSource:
        alias = 'mock_alias'
        sources = ['mock_source']
        targets = ['mock_target']
        @property
        def output_field(self):
            return User._meta.get_field('username')  # Using a field from User model

    return MockMultiColSource()

def test_as_sql_with_multicolumn_lookup(setup_related_lookup):
    compiler = SQLCompiler(compiler='mock_compiler')  # should match actual SQLCompiler in use
    connection = BaseDatabaseWrapper()  # use actual database wrapper

    related_lookup = RelatedIn(lhs=setup_related_lookup, rhs=[['value1', 'value2']])
    
    sql_output = related_lookup.as_sql(compiler, connection)

    assert isinstance(sql_output, tuple)
    assert 'mock_alias' in sql_output[0]  # Checking if alias is included in SQL
    assert 'value1' in sql_output[0]  # Check if input values appear in SQL output

def test_as_sql_with_direct_value_rhs(setup_related_lookup):
    compiler = SQLCompiler(compiler='mock_compiler')  # should match actual SQLCompiler in use
    connection = BaseDatabaseWrapper()  # use actual database wrapper

    related_lookup = RelatedIn(lhs=setup_related_lookup, rhs='direct_value')
    
    sql_output = related_lookup.as_sql(compiler, connection)

    assert isinstance(sql_output, tuple)
    assert 'direct_value' in sql_output[0]  # Check direct value appears in SQL

def test_as_sql_without_select_fields(setup_related_lookup):
    compiler = SQLCompiler(compiler='mock_compiler')  # should match actual SQLCompiler in use
    connection = BaseDatabaseWrapper()  # use actual database wrapper
    
    related_lookup = RelatedIn(lhs=setup_related_lookup, rhs=User.objects.all())
    related_lookup.rhs.clear_select_clause = lambda: None  # Defining function for rhs
   
    sql_output = related_lookup.as_sql(compiler, connection)

    assert isinstance(sql_output, tuple)
    assert 'mock_alias' in sql_output[0]  # Ensure alias is part of returned SQL