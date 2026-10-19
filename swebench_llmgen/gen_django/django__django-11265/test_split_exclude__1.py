import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.mark.parametrize("filter_expr, can_reuse, names_with_path, expected_condition", [
    (('child__name', 'foo'), set(), ['child'], None),  # Simplest case
    (('child__name', User.objects.create(username='foo').pk), set(['child']), ['child'], None),  # Use existing user
])
def test_split_exclude(filter_expr, can_reuse, names_with_path, expected_condition):
    # Create an instance of Query with the User model
    query = Query(User)

    # Call the split_exclude method
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # Check the condition returned
    assert isinstance(condition, query.where.__class__), "Condition should be of the same type as where node."

    # Additional assertions could depend on the exact structure of the `condition`
    # and what you expect it to be. For the current test, we can only assert its type,
    # as the expected structure is determined by the specifics of Django's Query classes.