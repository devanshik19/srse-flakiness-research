import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import DurationExpression
from django.db.models import DurationField
from django.db.models.sql.compiler import SQLCompiler
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from unittest.mock import MagicMock

class MockConnection:
    class ops:
        @staticmethod
        def format_for_duration_arithmetic(sql):
            return f"Formatted Duration SQL: {sql}"

@pytest.fixture
def mock_side():
    class MockSide:
        output_field = DurationField()

    return MockSide()

@pytest.fixture
def mock_compiler():
    class MockCompiler:
        def compile(self, side):
            return "SELECT * FROM some_table", []

    return MockCompiler()

@pytest.fixture
def mock_connection():
    return MockConnection()

def test_compile_duration_field(mock_side, mock_compiler, mock_connection):
    duration_expr = DurationExpression()
    sql, params = duration_expr.compile(mock_side, mock_compiler, mock_connection)
    assert sql == "Formatted Duration SQL: SELECT * FROM some_table"
    assert params == []

def test_compile_missing_output_field(mock_compiler, mock_connection):
    class MockSide:
        output_field = None
        
    duration_expr = DurationExpression()
    sql, params = duration_expr.compile(MockSide(), mock_compiler, mock_connection)
    assert sql == "SELECT * FROM some_table"
    assert params == []