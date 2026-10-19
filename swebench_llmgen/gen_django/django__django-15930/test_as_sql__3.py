import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.utils import OperationalError

class TestBaseExpression:
    
    def test_as_sql_raises_not_implemented_error(self):
        expression = BaseExpression()  # Assuming instantiation is possible for testing
        compiler = None  # No real compiler will be used in this test
        connection = None  # No real connection is needed
        
        with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
            expression.as_sql(compiler, connection)

    def test_as_sql_called_on_subclass(self):
        class TestExpression(BaseExpression):
            def as_sql(self, compiler, connection):
                return "SELECT *", []

        expression = TestExpression(output_field=None)
        compiler = F('username').get_source_expressions()  # Use an actual source expression as compiler
        connection = None  # No real connection needed to test output
        
        sql, params = expression.as_sql(compiler, connection)
        
        assert sql == "SELECT *"
        assert params == []