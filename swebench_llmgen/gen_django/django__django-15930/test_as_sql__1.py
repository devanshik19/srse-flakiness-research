import pytest
from django.db.models import F
from django.db.models.expressions import BaseExpression
from django.db import models

class TestBaseExpression(BaseExpression):

    def __init__(self, output_field):
        super().__init__(output_field)

    def as_sql(self, compiler, connection):
        raise NotImplementedError("Subclasses must implement as_sql()")

def test_base_expression_as_sql():
    expression = TestBaseExpression(output_field=F('username'))
    
    with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
        expression.as_sql(None, None)

    # Confirming other aspects of the class
    assert expression.output_field is F('username')
    assert isinstance(expression, BaseExpression)