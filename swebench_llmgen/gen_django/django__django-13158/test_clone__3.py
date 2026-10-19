import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

def test_clone():
    # Setup test data
    sql = "SELECT * FROM auth_user WHERE username = %s"
    using = 'default'
    params = ['testuser']
    
    # Create an original RawQuery instance
    original_query = RawQuery(sql, using, params=params)

    # Clone the original query
    cloned_query = original_query.clone(using)
    
    # Assert that the cloned query has the same SQL
    assert cloned_query.sql == original_query.sql
    # Assert that the cloned query uses the same database connection
    assert cloned_query.using == original_query.using
    # Assert that the cloned query has the same parameters
    assert cloned_query.params == original_query.params

    # Ensure that the original and cloned queries are distinct objects
    assert cloned_query is not original_query