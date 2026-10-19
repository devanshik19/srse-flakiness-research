import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.query import Query

@pytest.mark.parametrize(
    "names, expected_path_length, expected_final_field",
    [
        (['username'], 0, User._meta.get_field('username')),
        (['first_name'], 0, User._meta.get_field('first_name')),
        (['last_name'], 0, User._meta.get_field('last_name')),
        (['email'], 0, User._meta.get_field('email')),
        (['pk'], 0, User._meta.pk),
        (['profile'], 0, User._meta.get_field('profile')),  # Non-existent for User, should raise
    ]
)
def test_names_to_path(names, expected_path_length, expected_final_field):
    query = Query(model=User, alias_cols={})
    opts = User._meta

    if expected_final_field is User._meta.get_field('profile'):
        with pytest.raises(FieldError):
            query.names_to_path(names, opts)
    else:
        path, final_field, targets, remaining_names = query.names_to_path(names, opts)
        
        assert len(path) == expected_path_length
        assert final_field == expected_final_field
        assert remaining_names == []

def test_names_to_path_with_filtered_relation():
    user = User.objects.create(username='testuser', first_name='First', last_name='Last')
    query = Query(model=User, alias_cols={})
    opts = User._meta
    
    # Simulating a filtered relation; Assuming we have one
    query._filtered_relations = {"filtered_relation": None}  # No real class but for structure

    path, final_field, targets, remaining_names = query.names_to_path(['filtered_relation'], opts)
    
    assert len(path) == 0
    assert final_field is None
    assert remaining_names == ['filtered_relation']

def test_names_to_path_with_fail_on_missing():
    query = Query(model=User, alias_cols={})
    opts = User._meta

    with pytest.raises(FieldError):
        query.names_to_path(['non_existent_field'], opts, fail_on_missing=True)