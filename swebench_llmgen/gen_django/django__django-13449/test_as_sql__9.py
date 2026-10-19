import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression
from django.db.models.sql import compiler

class CustomExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        return "SELECT id FROM auth_user", []

def test_as_sql_not_implemented():
    expression = BaseExpression(output_field=None)
    with pytest.raises(NotImplementedError):
        expression.as_sql(None, None)

def test_custom_expression_as_sql():
    conn = connection
    expr = CustomExpression(output_field=None)
    
    # Simulate a query compiler
    query_compiler = compiler.SQLCompiler(query=None, connection=conn)
    sql, params = expr.as_sql(query_compiler, conn)

    assert sql == "SELECT id FROM auth_user"
    assert params == []