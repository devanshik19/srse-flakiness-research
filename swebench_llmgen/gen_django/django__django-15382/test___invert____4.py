import pytest
from django.contrib.auth.models import User
from django.db.models import Exists

@pytest.mark.parametrize("initial_negated, expected_negated", [
    (False, True),
    (True, False),
])
def test_invert_method(initial_negated, expected_negated):
    # Arrange
    queryset = User.objects.all()
    exists_expression = Exists(queryset, negated=initial_negated)

    # Act
    inverted_expression = ~exists_expression

    # Assert
    assert inverted_expression.negated == expected_negated
    assert inverted_expression.template == exists_expression.template
    assert inverted_expression.output_field == exists_expression.output_field
    assert inverted_expression.queryset == exists_expression.queryset