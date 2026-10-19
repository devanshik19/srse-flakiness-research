import pytest
from django.core.exceptions import FieldError
from django.db.models import Aggregate, IntegerField, F
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

class CustomAggregate(Aggregate):
    template = "%(function)s(%(expressions)s)"
    
    def __init__(self, expression, **extra):
        super().__init__(expression, output_field=IntegerField(), **extra)

def test_resolve_expression_with_aggregate_raises_fielderror():
    agg = CustomAggregate(F('id'))
    with pytest.raises(FieldError, match="Cannot compute .*('id'): 'id' is an aggregate"):
        agg.resolve_expression()

def test_resolve_expression_with_no_default():
    agg = CustomAggregate(F('id'))
    resolved = agg.resolve_expression()
    assert resolved is not None
    assert resolved.default is None

def test_resolve_expression_with_default():
    agg = CustomAggregate(F('id'), default=3)
    resolved = agg.resolve_expression()
    assert resolved is not None
    assert resolved.default == Coalesce(resolved, 3, output_field=IntegerField())

def test_resolve_expression_with_nested_aggregates_raises_fielderror():
    nested_agg = CustomAggregate(CustomAggregate(F('id')))
    with pytest.raises(FieldError, match="Cannot compute .*('id'): 'id' is an aggregate"):
        nested_agg.resolve_expression()