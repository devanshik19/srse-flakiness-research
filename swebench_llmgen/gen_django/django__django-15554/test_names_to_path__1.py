import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models import QuerySet
from django.db.models.sql.query import Query

@pytest.fixture
def query_instance():
    # Creates an instance of Query using the User model
    user_query = Query(User)
    return user_query

def test_names_to_path_single_field(query_instance):
    opts = User._meta
    names = ['username']
    path, final_field, targets, remaining_names = query_instance.names_to_path(names, opts)
    
    assert len(path) == 0  # No joins were made
    assert final_field.name == 'username'
    assert remaining_names == []

def test_names_to_path_related_field(query_instance):
    names = ['groups']  # Assuming User has a 'groups' related field
    opts = User._meta
    path, final_field, targets, remaining_names = query_instance.names_to_path(names, opts)
    
    assert len(path) > 0  # Joins are made for related fields
    assert hasattr(final_field, 'related_model')
    assert remaining_names == []

def test_names_to_path_with_invalid_field(query_instance):
    opts = User._meta
    invalid_names = ['invalid_field']
    
    with pytest.raises(FieldError) as excinfo:
        query_instance.names_to_path(invalid_names, opts, fail_on_missing=True)
    
    assert "Cannot resolve keyword 'invalid_field' into field" in str(excinfo.value)

def test_names_to_path_pk_field(query_instance):
    opts = User._meta
    names = ['pk']  # Testing 'pk' to resolve to the primary key field
    path, final_field, targets, remaining_names = query_instance.names_to_path(names, opts)

    assert len(path) == 0
    assert final_field.name == opts.pk.name
    assert remaining_names == []

def test_names_to_path_multiple_related_fields(query_instance):
    names = ['profile', 'address']  # Assuming User has a related profile and address
    opts = User._meta
    path, final_field, targets, remaining_names = query_instance.names_to_path(names, opts)

    assert len(path) > 0  # More than one join should be created
    assert remaining_names == []

def test_names_to_path_allow_many(query_instance):
    names = ['groups']
    opts = User._meta
    path, final_field, targets, remaining_names = query_instance.names_to_path(names, opts, allow_many=True)

    assert len(path) > 0
    assert final_field.related_model is not None
    assert remaining_names == []