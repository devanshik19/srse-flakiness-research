import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models import Aggregate, IntegerField
from django.db.models.functions import Coalesce

class CustomAggregate(Aggregate):
    def __init__(self, expression, **extra):
        super().__init__(expression, output_field=IntegerField(), **extra)

    def get_source_expressions(self):
        return [self.source_expressions[0]]

@pytest.mark.parametrize('summarize', [True, False])
def test_resolve_expression(summarize):
    user = User.objects.create(username='testuser')

    agg = CustomAggregate(base_expr := User.objects.values('id').annotate(Max('id')), name='custom_agg')
    
    # Test with valid default expression
    resolved = agg.resolve_expression()
    assert resolved is not None
    assert resolved.default == resolved

    # Test that FieldError is raised when the expression contains an aggregate
    with pytest.raises(FieldError):
        agg.get_source_expressions = lambda: [CustomAggregate('id')]
        agg.resolve_expression(summarize=summarize)

    # Test without aggregates in source expressions
    agg.get_source_expressions = lambda: [user]
    resolved = agg.resolve_expression(summarize=summarize)
    assert isinstance(resolved, Coalesce)