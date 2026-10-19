import pytest
from django.contrib.auth.models import User
from django.db.models import Exists

@pytest.mark.parametrize("negation, expected_negation", [
    (True, False),
    (False, True),
])
def test_invert_method(negation, expected_negation):
    # Create a sample queryset for the Exists expression
    queryset = User.objects.all()
    
    # Initialize the Exists object with a queryset and negation state
    exists_expr = Exists(queryset, negated=negation)

    # Invert the Exists expression
    inverted_expr = ~exists_expr

    # Check that the negated state has been inverted
    assert inverted_expr.negated == expected_negation
    assert inverted_expr.output_field is None  # Assuming default because not set