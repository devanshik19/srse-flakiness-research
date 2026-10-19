import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Exists

@pytest.mark.parametrize("initial_negated,expected_negated", [(False, True), (True, False)])
def test_invert(initial_negated, expected_negated):
    # Arrange: Create a queryset and an Exists instance
    queryset = User.objects.all()
    exists_expression = Exists(queryset, negated=initial_negated)

    # Act: Invert the Exists expression
    inverted_expression = ~exists_expression

    # Assert: Check the negation state
    assert inverted_expression.negated == expected_negated
    assert inverted_expression.template == exists_expression.template
    assert inverted_expression.output_field == exists_expression.output_field

    # Assert: Check that cloning does not affect the original
    assert exists_expression.negated == initial_negated