import pytest
from django.contrib.auth.models import User
from django.db.models import F, Expression
from django.db import connection

class TestBaseExpression(Expression):
    def as_sql(self, compiler, connection):
        raise NotImplementedError("Subclasses must implement as_sql()")

def test_base_expression_as_sql_not_implemented():
    compiler = User.objects.all().query.get_compiler(connection.alias)
    
    expr = TestBaseExpression(output_field=None)
    
    with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
        expr.as_sql(compiler, connection)

def test_custom_expression_as_sql():
    class CustomExpression(TestBaseExpression):
        def as_sql(self, compiler, connection):
            sql, params = super().as_sql(compiler, connection)
            return "SELECT * FROM auth_user", []

    expr = CustomExpression(output_field=None)
    compiler = User.objects.all().query.get_compiler(connection.alias)

    sql, params = expr.as_sql(compiler, connection)

    assert sql == "SELECT * FROM auth_user"
    assert params == []