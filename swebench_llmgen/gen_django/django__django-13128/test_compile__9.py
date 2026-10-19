import pytest
from django.contrib.auth.models import User
from django.db.models import DurationField, Expression, F
from django.db.models.expressions import DurationExpression
from django.db.models.sql.compiler import SQLCompiler

class MockCompiler:
    def compile(self, expression):
        return 'SELECT 1', []

class MockConnection:
    class ops:
        @staticmethod
        def format_for_duration_arithmetic(sql):
            return sql.replace('1', 'duration_sql')

@pytest.fixture
def duration_expression():
    return DurationExpression()

@pytest.fixture
def mock_side():
    class MockSide:
        output_field = DurationField()

        def __init__(self, output_field):
            self.output_field = output_field

    return MockSide(output_field=DurationField())

def test_compile_returns_duration_sql(duration_expression, mock_side):
    compiler = MockCompiler()
    connection = MockConnection()

    sql, params = duration_expression.compile(mock_side, compiler, connection)
    
    assert sql == 'duration_sql'
    assert params == []

def test_compile_raises_on_non_duration_field(duration_expression):
    class NonDurationFieldExpression(Expression):
        output_field = User

    compiler = MockCompiler()
    connection = MockConnection()
    side = NonDurationFieldExpression()

    with pytest.raises(Exception):
        duration_expression.compile(side, compiler, connection)