import pytest
from django.contrib.auth.models import User
from django.db.models import Exists

@pytest.mark.parametrize('negated', [True, False])
def test_invert_method(negated):
    # Arrange
    user_queryset = User.objects.all()
    exists_expression = Exists(user_queryset, negated=negated)

    # Act
    inverted_expression = ~exists_expression

    # Assert
    assert inverted_expression.negated is not negated
    assert isinstance(inverted_expression, Exists)
    assert inverted_expression.template == exists_expression.template
    assert inverted_expression.output_field == exists_expression.output_field