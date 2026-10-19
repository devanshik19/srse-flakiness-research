import pytest
from django.db import connection
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression


class TestBaseExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        # Custom as_sql implementation for testing purposes
        return "SELECT * FROM auth_user", []


def test_as_sql():
    expression = TestBaseExpression(output_field=F('username'))
    compiler = connection.ops.compiler
    sql, params = expression.as_sql(compiler, connection)
    
    assert sql == "SELECT * FROM auth_user"
    assert params == []

    # Ensure NotImplementedError is raised on the real BaseExpression
    with pytest.raises(NotImplementedError):
        BaseExpression().as_sql(None, None)