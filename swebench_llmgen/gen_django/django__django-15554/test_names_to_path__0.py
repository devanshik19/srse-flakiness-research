import pytest
from django.contrib.auth.models import User
from django.db.models import Manager
from django.db.models.sql.query import Query
from django.core.exceptions import FieldError

@pytest.fixture
def query_instance():
    # Create a Query instance for the User model
    user_model = User._meta
    return Query(model=user_model, alias_cols={})

@pytest.mark.parametrize(
    "names, expected_path_size, expected_final_field",
    [
        (["username"], 1, User._meta.get_field("username")),
        (["email"], 1, User._meta.get_field("email")),
        (["groups", "name"], 1, User._meta.get_field("name")),
        (["pk"], 1, User._meta.pk),
    ]
)
def test_names_to_path_valid_fields(query_instance, names, expected_path_size, expected_final_field):
    path, final_field, targets, remaining_names = query_instance.names_to_path(names, User._meta)
    
    assert len(path) == expected_path_size
    assert final_field == expected_final_field
    assert remaining_names == []

def test_names_to_path_invalid_field(query_instance):
    with pytest.raises(FieldError):
        query_instance.names_to_path(["nonexistent_field"], User._meta, fail_on_missing=True)

def test_names_to_path_invalid_relation(query_instance):
    with pytest.raises(FieldError):
        query_instance.names_to_path(["groups", "nonexistent_field"], User._meta, fail_on_missing=True)

def test_names_to_path_m2m(query_instance):
    path, final_field, targets, remaining_names = query_instance.names_to_path(["groups"], User._meta, allow_many=True)
    
    assert len(path) > 0
    assert final_field is None  # Assuming there is no single final field for M2M
    assert remaining_names == []