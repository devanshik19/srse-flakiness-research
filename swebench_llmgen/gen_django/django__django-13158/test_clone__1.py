import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.sql.query import RawQuery

@pytest.mark.parametrize("sql, using, expected_sql", [
    ("SELECT * FROM auth_user", "default", "SELECT * FROM auth_user"),
    ("SELECT * FROM auth_user WHERE id = %s", "default", "SELECT * FROM auth_user WHERE id = %s"),
])
def test_clone(sql, using, expected_sql):
    # Arrange
    params = [1]
    raw_query = RawQuery(sql, using, params)

    # Act
    cloned_query = raw_query.clone(using)

    # Assert
    assert cloned_query.sql == expected_sql
    assert cloned_query.params == params
    assert cloned_query.sql == raw_query.sql
    assert cloned_query.using == raw_query.using