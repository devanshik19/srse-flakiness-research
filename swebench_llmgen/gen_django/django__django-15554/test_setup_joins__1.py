import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query
from django.db.models.fields import Field
from django.core.exceptions import FieldError


@pytest.mark.parametrize(
    "names, can_reuse, allow_many, expect_exception",
    [
        (['username'], None, True, False),  # Normal case: valid field
        (['profile__bio'], None, True, False),  # Valid reverse relationship
        (['nonexistent_field'], None, True, True),  # Nonexistent field
        (['username'], None, False, False),  # Valid field, allow_many = False
        (['profile__nonexistent_field'], None, True, True),  # Nonexistent reverse relationship
        (['username__class'], None, True, True),  # Invalid lookup
    ],
)
def test_setup_joins(names, can_reuse, allow_many, expect_exception):
    user = User.objects.create_user(username='testuser', password='password')
    query = Query(model=User, alias_cols=False)
    opts = User._meta

    if expect_exception:
        with pytest.raises(FieldError):
            query.setup_joins(names, opts, alias='u', can_reuse=can_reuse, allow_many=allow_many)
    else:
        result = query.setup_joins(names, opts, alias='u', can_reuse=can_reuse, allow_many=allow_many)
        # Check the result structure if no exception was raised
        assert isinstance(result.final_field, Field) or result.final_field is None
        assert isinstance(result.opts, type(opts))
        assert isinstance(result.joins, list)
        assert isinstance(result.path, list)
        assert callable(result.transformer)