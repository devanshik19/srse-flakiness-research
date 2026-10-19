import pytest
from django.contrib.auth.models import User
from django.db.models import DurationField
from django.db.models.expressions import DurationExpression
from django.db.models.sql.compiler import SQLCompiler
from django.db import connection

class DummySide:
    def __init__(self, output_field):
        self.output_field = output_field

class DummyCompiler:
    def compile(self, side):
        return "SELECT * FROM auth_user", []

def test_compile_duration_field():
    # Setup DurationExpression and Dummy classes
    duration_field = DurationField()
    duration_expression = DurationExpression()

    # Test with DurationField output
    side = DummySide(output_field=duration_field)
    compiler = DummyCompiler()
    
    sql, params = duration_expression.compile(side, compiler, connection)

    assert sql == "SELECT * FROM auth_user"
    assert params == []

def test_compile_non_duration_field():
    # Setup DurationExpression and Dummy classes
    non_duration_field = User._meta.get_field('username')  # Example of a non-DurationField
    duration_expression = DurationExpression()

    # Test with a non-DurationField output
    side = DummySide(output_field=non_duration_field)
    compiler = DummyCompiler()

    sql, params = duration_expression.compile(side, compiler, connection)

    assert sql == "SELECT * FROM auth_user"
    assert params == []