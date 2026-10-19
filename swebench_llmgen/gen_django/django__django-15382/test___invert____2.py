import pytest
from django.contrib.auth.models import User
from django.db.models import Exists

@pytest.mark.parametrize("negated_initial, expected_negated", [
    (False, True),
    (True, False),
])
def test_invert(negated_initial, expected_negated):
    user_queryset = User.objects.all()
    exists_expression = Exists(user_queryset, negated=negated_initial)
    
    cloned_expression = ~exists_expression
    
    assert cloned_expression.negated == expected_negated
    assert cloned_expression.template == exists_expression.template
    assert cloned_expression.output_field == exists_expression.output_field