import pytest
from django.db.models import F
from django.db.models.expressions import BaseExpression
from django.db import connection
from django.contrib.auth.models import User


class CustomExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        return "SELECT * FROM auth_user", []


def test_as_sql_raises_not_implemented_error():
    expression = BaseExpression(output_field=F('username'))
    with pytest.raises(NotImplementedError):
        expression.as_sql(None, None)


def test_custom_expression_as_sql():
    expression = CustomExpression(output_field=F('username'))
    sql, params = expression.as_sql(None, connection)
    
    assert sql == "SELECT * FROM auth_user"
    assert params == []