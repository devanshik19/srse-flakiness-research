import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.fields import Field
from django.db.models.sql.datastructures import JoinInfo
from django.db.models.query_utils import Q

@pytest.fixture
def user_query():
    user_model = User
    return Query(user_model._meta)

def test_setup_joins_single_field(user_query):
    opts = user_query.get_meta()
    alias = user_query.get_initial_alias()
    names = ['username']
    
    join_info = user_query.setup_joins(names, opts, alias)
    
    assert isinstance(join_info, JoinInfo)
    assert join_info.final_field.name == 'username'
    assert join_info.joins == [alias]

def test_setup_joins_multiple_fields(user_query):
    opts = user_query.get_meta()
    alias = user_query.get_initial_alias()
    names = ['profile', 'bio']  # Assuming 'profile' is a related field

    with pytest.raises(FieldDoesNotExist):
        user_query.setup_joins(names, opts, alias)

def test_setup_joins_with_transforms(user_query):
    opts = user_query.get_meta()
    alias = user_query.get_initial_alias()
    names = ['username__length']  # Assuming 'length' is a valid transform function

    join_info = user_query.setup_joins(names, opts, alias)
    
    assert isinstance(join_info, JoinInfo)
    assert join_info.final_transformer is not None

def test_setup_joins_with_reverse_fk(user_query):
    opts = user_query.get_meta()
    alias = user_query.get_initial_alias()
    names = ['user_permissions']  # Assuming user_permissions is a reverse FK

    join_info = user_query.setup_joins(names, opts, alias)
    
    assert isinstance(join_info, JoinInfo)
    assert len(join_info.joins) > 1

def test_setup_joins_with_invalid_field(user_query):
    opts = user_query.get_meta()
    alias = user_query.get_initial_alias()
    names = ['invalid_field']

    with pytest.raises(FieldError):
        user_query.setup_joins(names, opts, alias)