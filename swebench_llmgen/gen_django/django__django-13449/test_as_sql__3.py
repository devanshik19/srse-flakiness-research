import pytest
from django.db import connection
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def as_sql(self, compiler, connection):
        return "SELECT * FROM auth_user", []

def test_as_sql():
    expression = TestBaseExpression(output_field=F('username'))
    sql, params = expression.as_sql(None, connection)

    assert sql == "SELECT * FROM auth_user"
    assert params == []

    # Test error for abstract method
    with pytest.raises(NotImplementedError):
        BaseExpression().as_sql(None, connection)