import pytest
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.expressions import BaseExpression
from django.db import connection, NotSupportedError

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field):
        super().__init__(output_field)

    def as_sql(self, compiler, connection):
        raise NotImplementedError("Subclasses must implement as_sql()")

def test_as_sql_not_implemented():
    expression = TestBaseExpression(output_field=Value('test'))
    
    with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
        expression.as_sql(None, connection)

def test_as_sql_with_custom_implementation(db):
    class CustomExpression(BaseExpression):
        def as_sql(self, compiler, connection):
            sql, params = compiler.compile(Value('custom_sql'))
            return sql, params
    
    custom_expression = CustomExpression(output_field=Value('custom'))
    sql, params = custom_expression.as_sql(None, connection)

    assert sql == "custom_sql"
    assert params == []

def test_as_sql_must_inherit_and_implement():
    with pytest.raises(TypeError):
        expression = BaseExpression(output_field=Value('test'))
        expression.as_sql(None, connection)