import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        return "SELECT * FROM auth_user", []

def test_as_sql_not_implemented():
    # Instantiate the BaseExpression for testing
    expr = BaseExpression(output_field=None)

    # Ensure that NotImplementedError is raised
    with pytest.raises(NotImplementedError):
        expr.as_sql(None, None)

def test_as_sql_overridden():
    # Instantiate the test subclass with an overridden as_sql method
    expr = TestBaseExpression(output_field=None)

    # Assuming the compiler and connection are provided by the Django ORM layer
    # Normally you would pass actual instances, here simplified for coverage
    sql, params = expr.as_sql(None, None)

    assert sql == "SELECT * FROM auth_user"
    assert params == []