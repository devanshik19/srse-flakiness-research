import pytest
from django.db.models import Expression
from django.db.models.expressions import BaseExpression
from django.db.models.sql.compiler import SQLCompiler
from django.db.backends.postgresql.base import DatabaseWrapper
from django.contrib.auth.models import User

class TestBaseExpression(BaseExpression):

    def __init__(self, output_field=None):
        super().__init__(output_field=output_field)

    def as_sql(self, compiler, connection):
        raise NotImplementedError("Subclasses must implement as_sql()")

def test_base_expression_as_sql_raises_not_implemented():
    expression = TestBaseExpression()
    compiler = SQLCompiler(None, None, None)  # Simplified for the test
    connection = DatabaseWrapper({})  # Simulate a connection
    with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
        expression.as_sql(compiler, connection)

def test_expression_subclass_as_sql():
    class ConcreteExpression(TestBaseExpression):
        def as_sql(self, compiler, connection):
            return "SELECT * FROM auth_user;", []

    expression = ConcreteExpression()
    compiler = SQLCompiler(None, None, None)
    connection = DatabaseWrapper({})
    
    sql, params = expression.as_sql(compiler, connection)
    
    assert sql == "SELECT * FROM auth_user;"
    assert params == []