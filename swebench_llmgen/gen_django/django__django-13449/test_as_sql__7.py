import pytest
from django.db import connection
from django.db.models import Expression


class CustomExpression(Expression):
    def as_sql(self, compiler, connection):
        return "SELECT *", []


def test_as_sql_not_implemented():
    expression = Expression()
    with pytest.raises(NotImplementedError):
        expression.as_sql(None, connection)


def test_custom_expression_as_sql():
    expression = CustomExpression()
    sql, params = expression.as_sql(None, connection)
    assert sql == "SELECT *"
    assert params == []