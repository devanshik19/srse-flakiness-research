import pytest
from django.db import connection
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression


class TestBaseExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        sql = "SELECT * FROM auth_user"
        params = []
        return sql, params


def test_as_sql():
    expression = TestBaseExpression(output_field=None)
    compiler = connection.ops.query
    sql, params = expression.as_sql(compiler, connection)

    assert sql == "SELECT * FROM auth_user"
    assert params == []

    # Check for NotImplementedError on BaseExpression
    with pytest.raises(NotImplementedError):
        base_expression = BaseExpression(output_field=None)
        base_expression.as_sql(compiler, connection)