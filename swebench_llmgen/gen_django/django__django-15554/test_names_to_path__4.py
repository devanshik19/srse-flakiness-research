import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.core.exceptions import FieldError

@pytest.fixture
def user_model():
    return User._meta

def test_names_to_path_single_field(user_model):
    query = Query(model=User)
    names = ['username']
    path, final_field, targets, remaining = query.names_to_path(names, user_model)
    
    assert len(path) == 0
    assert final_field.name == 'username'
    assert targets == (query.get_meta().get_field('username'),)
    assert remaining == []

def test_names_to_path_primary_key(user_model):
    query = Query(model=User)
    names = ['pk']
    path, final_field, targets, remaining = query.names_to_path(names, user_model)
    
    assert len(path) == 0
    assert final_field.name == 'id'
    assert targets == (query.get_meta().get_field('id'),)
    assert remaining == []

def test_names_to_path_invalid_field(user_model):
    query = Query(model=User)
    names = ['non_existent_field']
    
    with pytest.raises(FieldError) as exc_info:
        query.names_to_path(names, user_model, fail_on_missing=True)

    assert "Cannot resolve keyword 'non_existent_field'" in str(exc_info.value)

def test_names_to_path_filtered_relation(user_model):
    query = Query(model=User)
    # Simulating a filtered relation
    query._filtered_relations = {'group': None}
    names = ['group']
    
    with pytest.raises(FieldError) as exc_info:
        query.names_to_path(names, user_model, fail_on_missing=True)
    
    assert "Cannot resolve keyword 'group'" in str(exc_info.value)

def test_names_to_path_multi_join(user_model):
    query = Query(model=User)
    # Simulate an annotation or complicated situation
    query.annotation_select = {'some_annotation': User._meta.get_field('username')}

    names = ['some_annotation']
    path, final_field, targets, remaining = query.names_to_path(names, user_model)
    
    assert len(path) == 0
    assert final_field.name == 'username'
    assert targets == (query.annotation_select['some_annotation'].output_field,)
    assert remaining == []