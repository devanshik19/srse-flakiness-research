import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def setup_query():
    # Instantiate a base query object
    query = Query(User)
    return query

def test_join_with_reuse(setup_query):
    query = setup_query
    join1 = query.join_class()  # Create a join object
    join1.table_alias = 'join1'
    query.alias_map[join1.table_alias] = join1
    
    reuse_set = {join1.table_alias}
    
    # Join again with reuse
    result_alias = query.join(join1, reuse=reuse_set)
    
    # Ensure it reuses the existing alias
    assert result_alias == join1.table_alias

def test_join_without_reuse(setup_query):
    query = setup_query
    join1 = query.join_class()  # Create a join object
    join1.table_name = 'user'
    join1.table_alias = 'join1'
    
    # First join should create a new alias
    result_alias_1 = query.join(join1)
    assert result_alias_1 == 'join1'
    assert query.alias_map[result_alias_1] == join1

    # Create another join object
    join2 = query.join_class()
    join2.table_name = 'user'
    join2.table_alias = 'join2'
    
    # This should create a new alias as join1 is not in reuse set
    result_alias_2 = query.join(join2)
    assert result_alias_2 == 'join2'
    assert query.alias_map[result_alias_2] == join2

def test_join_with_nullable(setup_query):
    query = setup_query
    join1 = query.join_class()
    join1.table_name = 'user'
    join1.table_alias = 'join1'
    join1.nullable = True  # Mark nullable
    
    result_alias = query.join(join1)
    
    # Expect the join type to be LOUTER due to nullable
    assert query.alias_map[result_alias].join_type == 'LOUTER'
    assert result_alias == 'join1'