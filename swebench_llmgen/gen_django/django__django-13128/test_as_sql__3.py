import pytest
from django.db import connection
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field):
        super().__init__(output_field)

    def as_sql(self, compiler, connection):
        raise NotImplementedError("Subclasses must implement as_sql()")

def test_base_expression_as_sql_not_implemented():
    expr = TestBaseExpression(output_field=F('username'))

    with pytest.raises(NotImplementedError):
        expr.as_sql(None, connection)

def test_base_expression_as_sql_implementation():
    class CustomExpression(TestBaseExpression):
        def as_sql(self, compiler, connection):
            return "SELECT username FROM auth_user", []

    expr = CustomExpression(output_field=F('username'))
    sql, params = expr.as_sql(None, connection)

    assert sql == "SELECT username FROM auth_user"
    assert params == []