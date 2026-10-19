import pytest
from django.contrib.auth.models import User
from django.db.models import Expression
from django.db import connection

class TestBaseExpression(Expression):
    def __init__(self, output_field):
        super().__init__(output_field)

    def as_sql(self, compiler, connection):
        raise NotImplementedError("Subclasses must implement as_sql()")

def test_as_sql_not_implemented():
    expression = TestBaseExpression(output_field=None)
    with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
        expression.as_sql(None, connection)

def test_as_sql_with_custom_expression():
    class CustomExpression(TestBaseExpression):
        def as_sql(self, compiler, connection):
            return "SELECT * FROM my_table", []

    custom_expr = CustomExpression(output_field=None)
    sql, params = custom_expr.as_sql(None, connection)
    assert sql == "SELECT * FROM my_table"
    assert params == []