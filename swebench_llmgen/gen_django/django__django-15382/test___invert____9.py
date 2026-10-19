import pytest
from django.contrib.auth.models import User
from django.db.models import Exists

@pytest.fixture
def setup_queryset():
    # Create a User instance to query against
    User.objects.create(username='testuser1')
    User.objects.create(username='testuser2')
    return User.objects.filter(username='testuser1')

def test_invert_method(setup_queryset):
    queryset = setup_queryset
    exists_expression = Exists(queryset)

    # Ensure the original negated value is False
    assert exists_expression.negated is False

    # Invert the exists expression
    inverted_expression = ~exists_expression

    # Verify the new negated value is True
    assert inverted_expression.negated is True

    # Verify that the clone is indeed a separate instance
    assert exists_expression is not inverted_expression

    # Make sure other attributes remain unchanged
    assert exists_expression.template == inverted_expression.template
    assert exists_expression.output_field == inverted_expression.output_field