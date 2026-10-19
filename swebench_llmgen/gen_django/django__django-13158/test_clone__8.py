import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

def test_clone():
    # Arrange
    sql = "SELECT * FROM auth_user WHERE username = %s"
    using = "default"
    params = ["test_user"]
    
    original_query = RawQuery(sql, using, params=params)

    # Act
    cloned_query = original_query.clone(using)

    # Assert
    assert cloned_query.sql == original_query.sql
    assert cloned_query.using == original_query.using
    assert cloned_query.params == original_query.params
    assert cloned_query != original_query  # Ensure they are different instances