import pytest
from django.core.exceptions import FieldError
from django.db.models import Aggregate, Sum, Case, When, IntegerField
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

class CustomAggregate(Aggregate):
    def get_source_expressions(self):
        return [Sum('id')]  # Using an aggregate as a source expression for testing

def test_resolve_expression_without_summarize():
    agg = CustomAggregate()

    # Simulating the call with summarize=False
    result = agg.resolve_expression(summarize=False)

    assert isinstance(result, Coalesce)
    assert result.source == agg
    assert result.default is None

def test_resolve_expression_with_aggregate_in_source_expressions():
    agg = CustomAggregate()

    with pytest.raises(FieldError) as excinfo:
        agg.resolve_expression(summarize=False)

    assert "Cannot compute" in str(excinfo.value)

def test_resolve_expression_with_default_value():
    agg = CustomAggregate()

    # Setting a default value with an aggregate
    agg.default = 42
    result = agg.resolve_expression()

    assert isinstance(result, Coalesce)
    assert result.default == 42