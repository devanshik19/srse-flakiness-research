import pytest
from django.core.exceptions import FieldError
from django.db.models import Aggregate
from django.db.models.expressions import Case, When
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

class CustomAggregate(Aggregate):
    def get_source_expressions(self):
        return [self]

@pytest.mark.parametrize("summarize, contains_aggregate, expected_error", [
    (False, True, FieldError),   # Test for FieldError when contains_aggregate is True
    (False, False, None)         # Test for successful resolution when no aggregates are present
])
def test_resolve_expression(summarize, contains_aggregate, expected_error):
    aggregate = CustomAggregate()
    if contains_aggregate:
        aggregate.contains_aggregate = True
    else:
        aggregate.contains_aggregate = False

    # Prepare a dummy query expression
    query = Case(
        When(pk=1, then="some value"),
        default="default value"
    )
    aggregate.set_source_expressions([query])
    
    if expected_error:
        with pytest.raises(expected_error):
            aggregate.resolve_expression(summarize=summarize)
    else:
        resolved = aggregate.resolve_expression(summarize=summarize)
        assert resolved is not None
        assert isinstance(resolved, Coalesce)
        assert resolved._output_field_or_none == aggregate._output_field_or_none