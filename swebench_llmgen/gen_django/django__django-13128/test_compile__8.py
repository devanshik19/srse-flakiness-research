import pytest
from django.db.models import DurationField, Value
from django.db.models.expressions import DurationExpression
from django.db.models.sql.compiler import SQLCompiler
from django.db import connection
from django.contrib.auth.models import User

class MockCompiler(SQLCompiler):
    def compile(self, side):
        return 'SELECT 1', []

@pytest.fixture
def duration_expression():
    return DurationExpression()

def test_compile_with_duration_field(duration_expression):
    user = User.objects.create(username='testuser')
    side = Value(datetime.timedelta(days=1), output_field=DurationField())
    compiler = MockCompiler(None, None, None)
    
    sql, params = duration_expression.compile(side, compiler, connection)
    
    assert sql == 'SELECT 1'
    assert params == []

def test_compile_without_duration_field(duration_expression):
    user = User.objects.create(username='testuser')
    side = Value('non_duration', output_field=Value)  # Using a non-DurationField
    compiler = MockCompiler(None, None, None)
    
    sql, params = duration_expression.compile(side, compiler, connection)
    
    assert sql == 'SELECT 1'
    assert params == []