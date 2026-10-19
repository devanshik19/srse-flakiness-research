import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression


class TestBaseExpression:
    
    def test_as_sql_not_implemented(self):
        expression = BaseExpression(output_field=None)
        
        with pytest.raises(NotImplementedError):
            expression.as_sql(compiler=None, connection=None)