import pytest
from django.db.models import expressions
from django.db import connection

class TestBaseExpression:

    def test_as_sql_not_implemented(self):
        expr = expressions.BaseExpression(output_field=None)

        with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
            expr.as_sql(compiler=None, connection=connection)