import pytest
from django.db.models import Expression, F
from django.contrib.auth.models import User

class TestBaseExpression(Expression):
    def __init__(self, output_field):
        super().__init__(output_field)

    def as_sql(self, compiler, connection):
        return "SELECT *", []

def test_as_sql_not_implemented():
    expr = BaseExpression(None)
    with pytest.raises(NotImplementedError):
        expr.as_sql(None, None)

def test_test_base_expression_as_sql():
    compiler = None  # Use an appropriate mock/compiler here if needed
    connection = None  # Use an appropriate mock/connection here if needed
    expression = TestBaseExpression(F('username'))
    sql, params = expression.as_sql(compiler, connection)
    assert sql == "SELECT *"
    assert params == []

def test_base_expression_as_sql_custom_logic():
    class CustomSqlExpression(TestBaseExpression):
        def as_sql(self, compiler, connection):
            return "SELECT count(*)", []

    custom_expr = CustomSqlExpression(F('username'))
    sql, params = custom_expr.as_sql(None, None)
    assert sql == "SELECT count(*)"
    assert params == []