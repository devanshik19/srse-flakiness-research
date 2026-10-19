import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

def test_raw_query_clone():
    # Arrange
    sql = "SELECT * FROM auth_user"
    using = "default"
    params = {}
    original_query = RawQuery(sql, using, params=params)
    
    # Act
    cloned_query = original_query.clone(using)
    
    # Assert
    assert cloned_query.sql == original_query.sql
    assert cloned_query.params == original_query.params
    assert cloned_query.using == original_query.using
    assert cloned_query is not original_query  # Ensure it is a different instance