import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

def test_clone_method():
    # Arrange
    sql_query = "SELECT * FROM auth_user WHERE username = %s"
    using_db = "default"
    params = [User.objects.first().username]
    
    original_query = RawQuery(sql_query, using_db, params=params)
    
    # Act
    cloned_query = original_query.clone(using_db)

    # Assert
    assert cloned_query.sql == original_query.sql
    assert cloned_query.params == original_query.params
    assert cloned_query.__class__ is original_query.__class__
    assert cloned_query is not original_query  # Ensure it's a different instance