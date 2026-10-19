import pytest
from django.contrib.auth.models import User
from django.db.models import Func
from django.db.models.sql.compiler import SQLCompiler
from django.db import connection

class CustomExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        return "SELECT *", []

def test_as_sql_not_implemented():
    with pytest.raises(NotImplementedError):
        expression = BaseExpression()
        expression.as_sql(None, None)

def test_custom_expression_as_sql():
    compiler = SQLCompiler(None, None, connection)
    expression = CustomExpression(None)
    sql, params = expression.as_sql(compiler, connection)
    assert sql == "SELECT *"
    assert params == []