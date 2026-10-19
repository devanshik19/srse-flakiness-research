import pytest
from django.db.models import QuerySet, F, OuterRef, Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.mark.parametrize(
    "filter_expr, expected_condition, expected_inner",
    [
        (('child__name', 'foo'), None, False),  # Example case
        (('username', 'testuser'), None, False),  # simple case with User model
    ]
)
def test_split_exclude(filter_expr, expected_condition, expected_inner):
    user = User.objects.create(username='testuser')
    query = Query(User)

    # Simulating can_reuse and names_with_path for testing
    can_reuse = set()
    names_with_path = []

    # Call the split_exclude method
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # Assert the conditions and inner needed check
    assert condition is expected_condition
    assert needed_inner is expected_inner