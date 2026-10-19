import pytest
from django.contrib.auth.models import User
from django.db.models import DurationField
from django.db.models.expressions import DurationExpression
from django.db.models.sql.compiler import SQLCompiler
from django.db.backends.base.base import BaseDatabaseWrapper

class DummyCompiler(SQLCompiler):
    def compile(self, expression):
        return 'SELECT 1', []

class DummyConnection(BaseDatabaseWrapper):
    class ops:
        @staticmethod
        def format_for_duration_arithmetic(sql):
            return sql.replace('SELECT', 'SELECT FORMAT')

@pytest.fixture
def duration_expression():
    return DurationExpression()

@pytest.fixture
def dummy_side():
    user = User.objects.create(username='testuser')
    return user._state

@pytest.fixture
def dummy_compiler():
    return DummyCompiler()

@pytest.fixture
def dummy_connection():
    return DummyConnection()

def test_compile_duration_field(duration_expression, dummy_side, dummy_compiler, dummy_connection):
    dummy_side.output_field = DurationField()
    sql, params = duration_expression.compile(dummy_side, dummy_compiler, dummy_connection)

    assert sql == 'SELECT FORMAT 1'
    assert params == []

def test_compile_non_duration_field(duration_expression, dummy_side, dummy_compiler, dummy_connection):
    dummy_side.output_field = None
    sql, params = duration_expression.compile(dummy_side, dummy_compiler, dummy_connection)

    assert sql == 'SELECT 1'
    assert params == []