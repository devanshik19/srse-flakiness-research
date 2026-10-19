import pytest
from django.db import connection
from django.db.models import Expression
from django.contrib.auth.models import User

class TestBaseExpression(Expression):
    def as_sql(self, compiler, connection):
        return "SELECT * FROM auth_user", []

def test_as_sql_method():
    expression = TestBaseExpression(output_field=None)
    compiler = connection.query.compiler
    sql, params = expression.as_sql(compiler, connection)

    assert sql == "SELECT * FROM auth_user"
    assert params == []