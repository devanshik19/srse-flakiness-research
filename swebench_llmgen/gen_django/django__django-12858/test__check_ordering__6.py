import pytest
from django.core import checks
from django.contrib.auth.models import User

class TestModelOrderingCheck:

    @pytest.mark.parametrize("ordering, expected_errors", [
        (None, []),  # No ordering
        ([], []),    # Empty list
        (['username'], []),  # Valid single field
        (['-username'], []), # Valid single field with negative order
        (['username', 'email'], []), # Valid multiple fields
        (['username', '?'], []), # Valid field ignoring '?'
        (['unknown_field'], [checks.Error("'ordering' refers to the nonexistent field, related field, or lookup 'unknown_field'.")]),  # Nonexistent field
        (['username', 'unknown_field'], [
            checks.Error("'ordering' refers to the nonexistent field, related field, or lookup 'unknown_field'.")
        ]),  # Mixed valid and invalid fields
        ([1, 2], [checks.Error("'ordering' must be a tuple or list (even if you want to order by only one field).")]),  # Invalid type
    ])
    def test_check_ordering(self, ordering, expected_errors):
        # Mock the model's _meta attributes for testing
        User._meta.ordering = ordering
        User._meta.order_with_respect_to = None  # No relationship order

        errors = User._check_ordering()
        assert errors == expected_errors