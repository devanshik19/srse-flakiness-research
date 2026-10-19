import pytest
from django.db.models import Expression
from django.contrib.auth.models import User
from django.db.models.fields import CharField

class TestBaseExpression(Expression):
    def __init__(self, output_field=None):
        self.output_field = output_field or CharField()

    def select_format(self, compiler, sql, params):
        if hasattr(self.output_field, 'select_format'):
            return self.output_field.select_format(compiler, sql, params)
        return sql, params

class MockCompiler:
    pass

@pytest.mark.parametrize(
    "output_field, expected_sql, expected_params",
    [
        (CharField(select_format=lambda compiler, sql, params: (f"CASE WHEN {sql} THEN 1 ELSE 0 END", params)), "CASE WHEN user_id THEN 1 ELSE 0 END", []),
        (None, "SELECT *", [])
    ]
)
def test_select_format(output_field, expected_sql, expected_params):
    compiler = MockCompiler()
    expression = TestBaseExpression(output_field)
    
    sql, params = expression.select_format(compiler, "SELECT *", [])
    
    assert sql == expected_sql
    assert params == expected_params