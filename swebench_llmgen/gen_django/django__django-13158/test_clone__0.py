import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

def test_clone():
    # Setup initial RawQuery instance
    sql = "SELECT * FROM auth_user WHERE is_active = %s"
    using = 'default'
    params = [True]
    original_query = RawQuery(sql, using, params)

    # Clone the RawQuery instance
    cloned_query = original_query.clone(using)

    # Assertions to ensure the clone has the same SQL and parameters
    assert cloned_query.sql == original_query.sql
    assert cloned_query.params == original_query.params
    assert cloned_query.using == original_query.using
    
    # Ensure that the cloned instance is a different object
    assert cloned_query is not original_query