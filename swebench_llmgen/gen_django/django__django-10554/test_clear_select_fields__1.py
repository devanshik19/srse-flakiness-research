import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_clear_select_fields():
    # Create a Query instance using a User model
    user = User.objects.first()
    query = Query(model=User, where=None)
    
    # Simulating initial state with select fields
    query.select = ('username', 'email')
    query.values_select = ('username',)

    # Clear the select fields
    query.clear_select_fields()

    # Assert that select and values_select are empty
    assert query.select == ()
    assert query.values_select == ()

    # Ensure that no other state is affected
    assert query.alias_prefix is not None
    assert query.subq_aliases is not None
    assert query.compiler is not None