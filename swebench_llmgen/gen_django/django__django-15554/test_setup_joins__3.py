import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.query import Query

def test_setup_joins():
    query = Query(model=User)

    # Test with valid field names
    names = ['username']
    opts = User._meta
    alias = query.get_initial_alias()
    result = query.setup_joins(names, opts, alias)

    assert result is not None
    assert result.final_field.name == 'username'
    assert len(result.joins) == 1  # No joins for a simple field
    assert result.opts == opts

    # Test with a relationship (User has a foreign key to groups)
    names = ['groups']
    result = query.setup_joins(names, opts, alias)

    assert result is not None
    assert len(result.joins) > 1  # Expect joins due to related model
    assert result.final_field.name == 'groups'

    # Check with non-existing field names
    with pytest.raises(FieldDoesNotExist):
        names = ['invalid_field']
        query.setup_joins(names, opts, alias)

    # Test with multiple fields and lookup
    names = ['groups', 'name']
    result = query.setup_joins(names, opts, alias)
    
    assert result is not None
    assert result.final_field.name == 'name'  # Final field should be the last one in the path
    assert 'groups' in result.joins  # The join for 'groups' should exist