import pytest
from django.db import connection
from django.db.models import Expression
from django.contrib.auth.models import User

class TestBaseExpression:

    def test_as_sql_not_implemented(self):
        expression = Expression()  # Create an instance of a suitable subclass of BaseExpression
        with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
            expression.as_sql(None, connection)

    def test_as_sql_with_subclass(self):
        class ConcreteExpression(Expression):
            def as_sql(self, compiler, connection):
                return "SELECT * FROM my_table", []

        compiler = connection.ops.compiler  # Get the compiler from the connection
        expression = ConcreteExpression(output_field=None)  # Using a concrete subclass
        sql, params = expression.as_sql(compiler, connection)

        assert sql == "SELECT * FROM my_table"
        assert params == []