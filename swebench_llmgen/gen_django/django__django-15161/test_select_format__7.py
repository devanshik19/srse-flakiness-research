import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class MockOutputField:
    def select_format(self, compiler, sql, params):
        return f"SELECT {sql}", params

@pytest.fixture
def base_expression_with_output_field():
    expression = BaseExpression(output_field=MockOutputField())
    return expression

@pytest.fixture
def base_expression_without_output_field():
    expression = BaseExpression(output_field=None)
    return expression

def test_select_format_with_output_field(base_expression_with_output_field):
    sql = "username"
    params = []
    compiler = None  # Assuming compiler is not needed for this test
    formatted_sql, formatted_params = base_expression_with_output_field.select_format(compiler, sql, params)
    
    assert formatted_sql == "SELECT username"
    assert formatted_params == []

def test_select_format_without_output_field(base_expression_without_output_field):
    sql = "username"
    params = []
    compiler = None  # Assuming compiler is not needed for this test
    formatted_sql, formatted_params = base_expression_without_output_field.select_format(compiler, sql, params)
    
    assert formatted_sql == "username"
    assert formatted_params == []