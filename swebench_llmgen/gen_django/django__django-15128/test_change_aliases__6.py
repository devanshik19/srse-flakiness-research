import copy
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode

def test_change_aliases():
    # Setup
    user_alias_map = {
        'u': 'user',
        'id': 'user_id',
    }
    
    # Create a query object
    query = Query(User)
    
    # Add select and where clauses to the query
    query.select = (query._get_col(query.get_initial_alias(), 'username', 'u'),)
    query.where = WhereNode()
    query.where.add(query._get_col(query.get_initial_alias(), 'id', 'id'), 'AND')

    # Store the state before change
    original_select = copy.deepcopy(query.select)
    original_where = copy.deepcopy(query.where)

    # Execute the method to change aliases
    query.change_aliases(user_alias_map)

    # Check if the select part is updated correctly
    assert query.select != original_select
    assert all(col.alias == 'user' for col in query.select)

    # Check if the where clause is updated correctly
    assert query.where != original_where
    assert any(col.alias == 'user_id' for col in query.where.children)
    
    # Check if alias_map has been updated
    assert 'user' in query.alias_map
    assert 'user_id' in query.alias_map
    assert 'u' not in query.alias_map
    assert 'id' not in query.alias_map

    # Check external aliases
    assert query.external_aliases['user'] is True
    assert query.external_aliases['user_id'] is True