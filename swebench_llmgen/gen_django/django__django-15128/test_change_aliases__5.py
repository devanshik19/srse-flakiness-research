import copy
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db import connections

def test_change_aliases():
    # Setup for Query with a mock User model
    user = User.objects.create_user(username='testuser', password='testpass')
    
    # Create an instance of Query
    query = Query(model=User, alias_cols=("id", "username"))

    # Initial state of aliases
    old_alias = 'user_id'
    new_alias = 'account_id'
    query.alias_map = {
        old_alias: query.get_initial_alias(),
    }
    query.alias_refcount = {
        old_alias: 1,
    }
    query.external_aliases = {
        old_alias: False,
    }

    # Create mock internal structures
    query.where = copy.deepcopy(query)  # Use a deepcopy to prevent mutations
    query.where.relabel_aliases = lambda change_map: None  # Mock relabel_aliases

    # Prepare change_map
    change_map = {
        old_alias: new_alias,
    }

    # Perform the alias change
    query.change_aliases(change_map)
    
    # Assertions to check the new state
    assert new_alias in query.alias_map
    assert old_alias not in query.alias_map
    assert query.alias_refcount[new_alias] == 1
    assert new_alias in query.external_aliases and query.external_aliases[new_alias] is True

    # Ensure properties in where, select and group_by have been relabeled
    assert query.where.relabel_aliases.called
    assert query.select == tuple()  # Expecting empty as it's not set
    assert query.group_by == tuple()  # Expecting empty as it's not set
    
    # Test with annotations
    query.annotations = {old_alias: "some_expression"}
    query.change_aliases(change_map)
    assert new_alias in query.annotations
    assert old_alias not in query.annotations