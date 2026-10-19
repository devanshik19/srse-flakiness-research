import pytest
from django.db.models import Aggregate, IntegerField
from django.db.models import QuerySet
from django.db.models.expressions import BaseExpression
from django.contrib.auth.models import User


class CustomExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        return "1", []


def test_as_sql_not_implemented():
    expression = BaseExpression(output_field=IntegerField())
    with pytest.raises(NotImplementedError):
        expression.as_sql(None, None)


def test_as_sql_custom_expression():
    custom_expression = CustomExpression(output_field=IntegerField())
    sql, params = custom_expression.as_sql(None, None)
    assert sql == "1"
    assert params == []


def test_standard_expression_sql_in_query():
    user = User.objects.create(username='testuser')
    queryset = User.objects.annotate(custom_field=CustomExpression(output_field=IntegerField()))
    
    # Ensure the queryset returns the expected results (this uses the custom expression)
    assert isinstance(queryset, QuerySet)
    assert queryset.filter(custom_field=1).exists() == True