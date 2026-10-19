import pytest
from django.contrib.auth.models import User
from django.db.models import expressions, F

class TestBaseExpression:
    
    class DummyOutputField:
        def select_format(self, compiler, sql, params):
            return f"SELECT {sql}", params

    def test_select_format_with_custom_output_field(self):
        expr = expressions.BaseExpression(output_field=self.DummyOutputField())
        sql, params = expr.select_format(None, 'username', [])
        
        assert sql == "SELECT username"
        assert params == []

    def test_select_format_without_custom_output_field(self):
        expr = expressions.BaseExpression(output_field=None)
        sql, params = expr.select_format(None, 'username', [])
        
        assert sql == 'username'
        assert params == []