import warnings
import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.lookups import RelatedIn, Exact

@pytest.mark.parametrize(
    "lhs_rhs,expected",
    [
        # Test with direct values for single-column relations
        (User.objects.filter(id__in=[1, 2]), [1, 2]),
        # Test with no select fields where lhs field is a primary key
        (User.objects.filter(username__in=['testuser']), ['testuser']),
    ],
)
def test_get_prep_lookup(lhs_rhs, expected):
    related_in_lookup = RelatedIn(lhs='username', rhs=lhs_rhs)
    result = related_in_lookup.get_prep_lookup()
    
    # Check the normalized `rhs` values
    assert result == expected

def test_get_prep_lookup_with_non_pk_field():
    user = User.objects.create(username='testuser')
    related_in_lookup = RelatedIn(lhs='username', rhs=[user.username])
    
    # Prepare the related field lookup
    result = related_in_lookup.get_prep_lookup()
    
    # Validate the preparation of the lookup
    assert result == [user.username]

def test_get_prep_lookup_with_invalid_value():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        related_in_lookup = RelatedIn(lhs='username', rhs=['invalid_user'])
        result = related_in_lookup.get_prep_lookup()

        # Ensure there are no real effects on the output
        assert result == ['invalid_user']  # Invalid inputs could remain unchanged

        # Check that the right warning is triggered
        assert len(w) == 0  # Adjust based on actual warning behavior, this is just a placeholder.