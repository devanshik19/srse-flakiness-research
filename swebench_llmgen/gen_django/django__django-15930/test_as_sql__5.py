import pytest
from django.db.models import Expression
from django.db.models import Value
from django.db.models.sql.compiler import SQLCompiler
from django.contrib.auth.models import User

class TestBaseExpression(Expression):
    def __init__(self, output_field):
        super().__init__(output_field=output_field)

    def as_sql(self, compiler, connection):
        return "SELECT 1", []

def test_as_sql_not_implemented():
    expr = BaseExpression()
    with pytest.raises(NotImplementedError):
        expr.as_sql(None, None)

def test_as_sql_with_valid_compiler_and_connection():
    user_expr = TestBaseExpression(output_field=Value('field'))
    compiler = SQLCompiler(connection=connection, query=None, using=None)
    
    sql, params = user_expr.as_sql(compiler, connection)
    
    assert sql == "SELECT 1"
    assert params == []