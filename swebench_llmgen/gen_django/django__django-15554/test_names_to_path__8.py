import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.query import Query
from django.core.exceptions import FieldError, FieldDoesNotExist

@pytest.mark.parametrize(
    "names, allow_many, fail_on_missing, expected_path, expected_field, expected_targets, expected_remaining",
    [
        (['username'], True, False, [], User._meta.get_field('username'), [User._meta.get_field('username')], []),
        (['id'], True, False, [], User._meta.get_field('id'), [User._meta.get_field('id')], []),
        (['NonExistentField'], True, True, FieldError, None, None, None),
        (['username', 'NonExistentField'], True, True, FieldError, None, None, ['NonExistentField']),
        (['first_name', 'last_name'], True, False, [], User._meta.get_field('last_name'), [User._meta.get_field('last_name')], []),
        (['pk'], True, False, [], User._meta.pk, [User._meta.pk], []),
    ]
)
def test_names_to_path(names, allow_many, fail_on_missing, expected_path, expected_field, expected_targets, expected_remaining):
    query = Query(User)  # Assuming that Query takes a model
    opts = User._meta

    if isinstance(expected_path, type) and expected_path is FieldError:
        with pytest.raises(FieldError):
            query.names_to_path(names, opts, allow_many, fail_on_missing)
    else:
        path, final_field, targets, remaining = query.names_to_path(names, opts, allow_many, fail_on_missing)
        assert path == expected_path
        assert final_field == expected_field
        assert targets == expected_targets
        assert remaining == expected_remaining