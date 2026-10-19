import pytest
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.contrib.auth.models import User

class TestSQLCompiler:

    @pytest.fixture
    def setup_compiler(self):
        # Create a simple query to compile
        user_query = User.objects.all()
        compiler = SQLCompiler(user_query.query, connection, using=connection.alias)
        return compiler

    def test_execute_sql_no_query(self, setup_compiler):
        compiler = setup_compiler
        # Simulate an empty query
        compiler.connection = None
        
        with pytest.raises(EmptyResultSet):
            result = compiler.execute_sql()

    def test_execute_sql_single(self, setup_compiler):
        compiler = setup_compiler
        result = compiler.execute_sql(result_type='SINGLE')
        assert isinstance(result, tuple)
    
    def test_execute_sql_multi(self, setup_compiler):
        compiler = setup_compiler
        result = compiler.execute_sql(result_type='MULTI')
        assert isinstance(result, list)

    def test_execute_sql_cursor(self, setup_compiler):
        compiler = setup_compiler
        cursor_result = compiler.execute_sql(result_type='CURSOR')
        assert cursor_result is not None
        assert cursor_result.description is not None

    def test_execute_sql_no_results(self, setup_compiler):
        compiler = setup_compiler
        # Alter the query to ensure no results
        User.objects.all().delete()
        result = compiler.execute_sql(result_type='NO_RESULTS')
        assert result is None