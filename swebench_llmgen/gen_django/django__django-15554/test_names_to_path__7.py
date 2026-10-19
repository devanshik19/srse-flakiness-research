import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.fields import FieldDoesNotExist, FieldError
from django.db.models.sql.where import MultiJoin

@pytest.fixture
def user_model():
    return User._meta

def test_names_to_path_single_field(user_model):
    query = Query(model=User)
    names = ['username']
    path, final_field, targets, remaining_names = query.names_to_path(names, user_model)
    
    assert len(path) == 0
    assert final_field.name == 'username'
    assert targets == (user_model.get_field('username'),)
    assert remaining_names == []

def test_names_to_path_primary_key(user_model):
    query = Query(model=User)
    names = ['pk']
    path, final_field, targets, remaining_names = query.names_to_path(names, user_model)

    assert len(path) == 0
    assert final_field.name == 'id'
    assert targets == (user_model.pk,)
    assert remaining_names == []

def test_names_to_path_filtered_relation(user_model):
    query = Query(model=User)
    query._filtered_relations = {'filtered_user': user_model}
    names = ['filtered_user']
    path, final_field, targets, remaining_names = query.names_to_path(names, user_model)

    assert len(path) == 0
    assert final_field == user_model.get_field('filtered_user')
    assert targets == (user_model.get_field('filtered_user'),)
    assert remaining_names == []

def test_names_to_path_failure_on_missing(user_model):
    query = Query(model=User)
    names = ['nonexistent_field']
    with pytest.raises(FieldError) as exc_info:
        query.names_to_path(names, user_model, fail_on_missing=True)

    assert "Cannot resolve keyword 'nonexistent_field' into field." in str(exc_info.value)

def test_names_to_path_multi_join(user_model):
    query = Query(model=User)
    names = ['groups']  # assuming User has a many-to-many relationship with Group
    path, final_field, targets, remaining_names = query.names_to_path(names, user_model, allow_many=False)

    assert len(path) > 0
    assert isinstance(path[0], MultiJoin)
    assert final_field == user_model.get_field('groups')
    assert targets == (user_model.get_field('groups'),)
    assert remaining_names == []