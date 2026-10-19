import pytest
from django.contrib.auth.models import User
from django.db.models import Expression

class TestBaseExpression(Expression):
    def __init__(self, output_field=None):
        super().__init__(output_field)

    def get_db_converters(self, connection):
        return []

def test_as_sql():
    compiler = User.objects.query.get_compiler(connection.alias)  # Get the compiler for the User model query
    connection = compiler.connection  # Get the connection from the compiler

    expression = TestBaseExpression()
    
    with pytest.raises(NotImplementedError):
        expression.as_sql(compiler, connection)

    # Here we can also test if it correctly raises the exception for subclasses that don't implement as_sql
    class SubclassExpression(TestBaseExpression):
        pass

    subclass_expression = SubclassExpression()
    
    with pytest.raises(NotImplementedError):
        subclass_expression.as_sql(compiler, connection)