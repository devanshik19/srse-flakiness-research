import pytest
from django.contrib.auth.models import User
from django.db.models import DurationField, Expression
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode

class DurationExpression(Expression):
    def compile(self, side, compiler, connection):
        try:
            output = side.output_field
        except FieldError:
            pass
        else:
            if output.get_internal_type() == 'DurationField':
                sql, params = compiler.compile(side)
                return connection.ops.format_for_duration_arithmetic(sql), params
        return compiler.compile(side)

class MockCompiler(SQLCompiler):
    def compile(self, *args, **kwargs):
        return "SELECT *", []

@pytest.fixture
def duration_expression():
    return DurationExpression()

@pytest.fixture
def mock_query():
    return Query()

@pytest.fixture
def mock_connection():
    class MockConnection:
        class ops:
            @staticmethod
            def format_for_duration_arithmetic(sql):
                return f"formatted({sql})"
    return MockConnection()

def test_compile_with_duration_field(duration_expression, mock_query, mock_connection):
    mock_query.add_filter(WhereNode(), "duration_field", DurationField())
    
    class MockSide:
        output_field = DurationField()

    compiler = MockCompiler(mock_query, connection=mock_connection)
    sql, params = duration_expression.compile(MockSide(), compiler, mock_connection)
    
    assert sql == "formatted(SELECT *)"
    assert params == []

def test_compile_without_duration_field(duration_expression, mock_query, mock_connection):
    mock_query.add_filter(WhereNode(), "non_duration_field", DurationField())
    
    class MockSide:
        output_field = DurationField()  # Still a DurationField

    compiler = MockCompiler(mock_query, connection=mock_connection)
    sql, params = duration_expression.compile(MockSide(), compiler, mock_connection)
    
    assert sql == "SELECT *"
    assert params == []