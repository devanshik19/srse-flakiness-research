import pytest
from django.db.models import Expression
from django.db.models.sql.compiler import SQLCompiler
from django.db import connection
from django.contrib.auth.models import User

class TestBaseExpression(Expression):
    def as_sql(self, compiler, connection):
        return "SELECT * FROM auth_user", []

def test_as_sql_not_implemented():
    expr = Expression()
    with pytest.raises(NotImplementedError):
        expr.as_sql(None, None)

def test_as_sql_implemented():
    expr = TestBaseExpression()
    compiler = SQLCompiler(connection, User.objects.all().query)
    sql, params = expr.as_sql(compiler, connection)
    assert sql == "SELECT * FROM auth_user"
    assert params == []