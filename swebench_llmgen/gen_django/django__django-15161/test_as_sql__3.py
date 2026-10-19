import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        return "SELECT *", []

def test_as_sql_not_implemented():
    # Testing if as_sql raises NotImplementedError
    with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
        BaseExpression().as_sql(None, None)

def test_as_sql_implemented():
    # Testing the custom implementation of as_sql
    expr = TestBaseExpression(output_field=None)
    sql, params = expr.as_sql(None, None)
    
    assert sql == "SELECT *"
    assert params == []

def test_expression_with_query():
    # Testing usage in a query (no specific behavior since as_sql is trivial)
    User.objects.create(username='testuser')
    
    query = User.objects.all()
    
    assert query.count() == 1