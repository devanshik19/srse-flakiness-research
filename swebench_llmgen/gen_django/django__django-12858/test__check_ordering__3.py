import pytest
from django.core import checks
from django.contrib.auth.models import User

@pytest.mark.parametrize("ordering, expected_errors", [
    (None, []),
    ([], []),
    (['username'], []),
    (['-username'], []),
    (['username', 'email'], []),
    (['-username', 'email'], []),
    (['username', 'non_existent_field'], [
        checks.Error(
            "'ordering' refers to the nonexistent field, related field, or lookup 'non_existent_field'.",
            obj=User,
            id='models.E015',
        )
    ]),
    (['-non_existent_field'], [
        checks.Error(
            "'ordering' refers to the nonexistent field, related field, or lookup '-non_existent_field'.",
            obj=User,
            id='models.E015',
        )
    ]),
    (['username', '?'], []),  # '?' should be filtered out
])
def test_check_ordering(ordering, expected_errors):
    User._meta.ordering = ordering
    User._meta.order_with_respect_to = None
    User._meta._ordering_clash = False

    errors = User._check_ordering()

    assert errors == expected_errors