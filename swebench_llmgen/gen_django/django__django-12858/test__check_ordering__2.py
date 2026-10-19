import pytest
from django.core import checks
from django.contrib.auth.models import User


class TestModelCheckOrdering:

    @pytest.mark.parametrize(
        "ordering, expected_errors",
        [
            ([ 'username' ], []),  # Valid ordering
            ([ '-username' ], []), # Valid ordering with reverse
            ([ 'username', 'email' ], []),  # Multiple valid fields
            ([ 'non_existent_field' ], [
                checks.Error(
                    "'ordering' refers to the nonexistent field, related field, or lookup 'non_existent_field'.",
                    obj=User,
                    id='models.E015',
                )
            ]),
            ([ 'username', 'non_existent_field' ], [
                checks.Error(
                    "'ordering' refers to the nonexistent field, related field, or lookup 'non_existent_field'.",
                    obj=User,
                    id='models.E015',
                )
            ]),
            ([ '?', 'email' ], []),  # Ignore '?'
            ([ 'pk' ], []),  # pk is allowed
            ([ '-pk' ], []),  # Reverse of pk is allowed
            ([ 'username', 'non_related_field' ], [
                checks.Error(
                    "'ordering' refers to the nonexistent field, related field, or lookup 'non_related_field'.",
                    obj=User,
                    id='models.E015',
                )
            ]),
        ]
    )
    def test_check_ordering(self, ordering, expected_errors):
        # Set the class attribute directly for testing
        User._meta.ordering = ordering
        
        # Call the focal function
        errors = User._check_ordering()

        # Check that the errors match expected
        assert errors == expected_errors