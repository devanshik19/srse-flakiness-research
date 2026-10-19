import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Expression

class TestBaseExpression(Expression):
    def as_sql(self, compiler, connection):
        return "SELECT *", []

def test_as_sql():
    compiler = connection.ops.compiler
    expression = TestBaseExpression(output_field=None)

    sql, params = expression.as_sql(compiler, connection)

    assert sql == "SELECT *"
    assert params == []