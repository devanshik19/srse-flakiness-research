import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.mark.parametrize("names, allow_many, expected", [
    (["username"], True, "username"),
    (["profile__bio"], True, "bio"),
    (["profile__bio"], False, "bio"),
])
def test_setup_joins(names, allow_many, expected):
    # Create a Query object for the User model
    query = Query(User._meta, alias_cols=False)
    alias = query.get_initial_alias()

    # Mock the options
    opts = User._meta

    # Execute setup_joins
    join_info = query.setup_joins(names, opts, alias, allow_many=allow_many)

    # Check if the final field name matches the expected result
    final_field_name = join_info.final_field.name
    assert final_field_name == expected

@pytest.mark.parametrize("names, expect_error", [
    (["username__icontains"], False),  # Valid lookup
    (["profile__non_existent_field"], True),  # Invalid lookup
])
def test_setup_joins_exceptions(names, expect_error):
    query = Query(User._meta, alias_cols=False)
    alias = query.get_initial_alias()
    opts = User._meta

    if expect_error:
        with pytest.raises(Exception):
            query.setup_joins(names, opts, alias, allow_many=True)
    else:
        join_info = query.setup_joins(names, opts, alias, allow_many=True)
        assert join_info is not None

def test_setup_joins_reusable_aliases():
    query = Query(User._meta, alias_cols=False)
    alias = query.get_initial_alias()
    opts = User._meta

    # Mocking reusable aliases
    can_reuse = {alias}

    # Execute setup_joins with reusable aliases
    join_info = query.setup_joins(['username'], opts, alias, can_reuse=can_reuse)

    # Assert that we got the correct join info
    assert join_info.join_type == "INNER"
    assert alias in join_info.joins