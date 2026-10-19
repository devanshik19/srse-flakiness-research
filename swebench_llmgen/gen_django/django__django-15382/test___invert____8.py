import pytest
from django.contrib.auth.models import User
from django.db.models import Exists

@pytest.mark.django_db
def test_invert_exists():
    # Create a sample user
    User.objects.create(username='test_user', password='password')

    # Create an Exists object for User model
    queryset = User.objects.all()
    exists_expression = Exists(queryset)

    # Verify initial state
    assert exists_expression.negated is False

    # Invert the Exists expression
    inverted_exists_expression = ~exists_expression

    # Verify the state of the inverted expression
    assert inverted_exists_expression.negated is True
    assert inverted_exists_expression.template == exists_expression.template
    assert inverted_exists_expression.output_field == exists_expression.output_field

    # Verify the original remains unchanged
    assert exists_expression.negated is False