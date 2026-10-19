import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def user_model():
    return User

def test_setup_joins_user_model(user_model):
    query_instance = Query(model=user_model)

    # Single field lookup: username
    names = ['username']
    opts = user_model._meta
    alias = query_instance.get_initial_alias()
    result = query_instance.setup_joins(names, opts, alias)

    assert result.final_field.name == 'username'
    assert len(result.joins) == 1

    # Multiple field lookups: username with transform
    names = ['username', 'upper']
    result = query_instance.setup_joins(names, opts, alias)

    assert result.final_field.name == 'username'
    assert len(result.joins) == 1

    # Test for a field that requires join
    names = ['profile', 'bio']  # Assuming 'profile' is a related field
    result = query_instance.setup_joins(names, opts, alias)

    assert result.final_field.name == 'bio'
    assert len(result.joins) > 1  # More joins expected due to relationship

    # Test with can_reuse argument
    can_reuse = {query_instance.get_initial_alias()}
    names = ['groups']
    result = query_instance.setup_joins(names, opts, alias, can_reuse=can_reuse)

    assert result.final_field.name == 'groups'
    assert len(result.joins) == 1

    # Test with allow_many = False
    with pytest.raises(FieldError):
        names = ['profile', 'users']  # assuming 'users' leads to a many-to-many
        query_instance.setup_joins(names, opts, alias, allow_many=False)

    # Edge case: Trailing lookups with an exception
    names = ['non_existent_field']
    
    with pytest.raises(FieldError):
        query_instance.setup_joins(names, opts, alias)