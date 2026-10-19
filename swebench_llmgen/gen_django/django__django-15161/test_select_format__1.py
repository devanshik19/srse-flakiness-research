import pytest
from django.contrib.auth.models import User
from django.db.models import Expression
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def __init__(self, output_field):
        super().__init__(output_field)

    def select_format(self, compiler, sql, params):
        if hasattr(self.output_field, 'select_format'):
            return self.output_field.select_format(compiler, sql, params)
        return sql, params

def test_select_format_with_custom_output_field():
    class CustomOutputField:
        def select_format(self, compiler, sql, params):
            return f"CASE WHEN {sql} THEN 1 ELSE 0 END", params

    custom_field = CustomOutputField()
    expression = TestBaseExpression(output_field=custom_field)

    sql, params = expression.select_format(None, 'user_id IS NOT NULL', [])
    assert sql == "CASE WHEN user_id IS NOT NULL THEN 1 ELSE 0 END"
    assert params == []

def test_select_format_without_custom_output_field():
    expression = TestBaseExpression(output_field=None)

    sql, params = expression.select_format(None, 'user_id IS NOT NULL', [])
    assert sql == 'user_id IS NOT NULL'
    assert params == []