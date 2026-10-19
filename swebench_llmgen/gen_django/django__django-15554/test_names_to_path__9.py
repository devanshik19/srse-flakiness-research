import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.query import Query
from django.core.exceptions import FieldError

@pytest.fixture
def user_model():
    return User

def test_names_to_path_single_field(user_model):
    query = Query(user_model)
    path, final_field, targets, remaining = query.names_to_path(['username'], user_model._meta)

    assert len(path) == 1
    assert final_field.name == 'username'
    assert targets == (user_model._meta.get_field('username'),)
    assert remaining == []

def test_names_to_path_primary_key(user_model):
    query = Query(user_model)
    path, final_field, targets, remaining = query.names_to_path(['pk'], user_model._meta)

    assert len(path) == 1
    assert final_field.name == 'id'
    assert targets == (user_model._meta.get_field('id'),)
    assert remaining == []

def test_names_to_path_filtered_relation(user_model):
    query = Query(user_model)
    user = user_model.objects.create(username='testuser')
    query._filtered_relations = {
        'user_profile': user
    }
    
    path, final_field, targets, remaining = query.names_to_path(['user_profile'], user_model._meta, allow_many=False)

    assert len(path) == 0  # No actual relation
    assert final_field is None
    assert targets == ()
    assert remaining == []

def test_names_to_path_fail_on_missing(user_model):
    query = Query(user_model)
    
    with pytest.raises(FieldError) as excinfo:
        query.names_to_path(['non_existent_field'], user_model._meta, fail_on_missing=True)

    assert "Cannot resolve keyword 'non_existent_field'" in str(excinfo.value)

def test_names_to_path_multiple_paths(user_model):
    query = Query(user_model)
    user = user_model.objects.create(username='testuser')

    # Example with a related field, may need to define a relation on User model.
    # Here we just use a made-up 'profile' relation for demonstration.
    # path, final_field, targets, remaining = query.names_to_path(['profile', 'bio'], user_model._meta)

    # Normally you'd need to assert against real existing paths and fields.
    # However, for the purpose of this test, we don't have a 'profile' relation.
    # Uncomment and modify the above lines when you have such relation in your model.

    # Example assertions if you have a profile related field
    # assert len(path) > 1  # Assuming 'profile' would correctly resolve
    # assert final_field.name == 'bio'  # Or whatever the final field would be
    # assert targets == (final_field,)  # And the proper target
    # assert remaining == []