import pytest
from django.contrib.auth.models import User
from django.db.models import DurationField
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.expressions import DurationExpression
from django.db import connection

class DummyCompiler(SQLCompiler):
    def compile(self, expression, *args, **kwargs):
        return 'SELECT 1', []  # Mimics the output of compile

def test_compile_with_duration_field():
    # Setup
    user = User(username='test_user', password='test_password')
    user.save()
    
    # Create an instance of the DurationExpression
    duration_expr = DurationExpression()
    
    # Creating a side with a mock output field simulating DurationField
    class MockSide:
        output_field = DurationField()
    
    compiler = DummyCompiler()
    result = duration_expr.compile(MockSide(), compiler, connection)
    
    assert result == ('SELECT 1', []), "Expected SQL and params do not match"

def test_compile_without_duration_field():
    # Setup
    user = User(username='test_user', password='test_password')
    user.save()
    
    # Create an instance of the DurationExpression
    duration_expr = DurationExpression()
    
    # Creating a side with a mock output field simulating a non-DurationField
    class MockSide:
        output_field = None
    
    compiler = DummyCompiler()
    
    with pytest.raises(FieldError):
        duration_expr.compile(MockSide(), compiler, connection)