import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

def test_clone():
    # Setup a RawQuery instance with sample SQL and params
    sql = 'SELECT * FROM auth_user WHERE username = %s'
    using = 'default'
    params = ['testuser']
    
    # Create an original RawQuery instance
    original_query = RawQuery(sql, using, params=params)
    
    # Clone the original RawQuery instance
    cloned_query = original_query.clone(using)
    
    # Assert that the original and cloned queries have the same SQL
    assert original_query.sql == cloned_query.sql
    
    # Assert that the original and cloned queries have the same params
    assert original_query.params == cloned_query.params
    
    # Assert that the original and cloned queries are not the same object
    assert original_query is not cloned_query
    
    # Assert that the using attribute is correctly passed
    assert cloned_query.using == using