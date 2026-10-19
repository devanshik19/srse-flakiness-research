import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

def test_clone():
    sql = "SELECT * FROM auth_user WHERE id = %s"
    using = 'default'
    params = [1]

    # Initialize the RawQuery object
    original_query = RawQuery(sql, using, params=params)

    # Clone the original query
    cloned_query = original_query.clone(using)

    # Assert that the cloned query has the same SQL
    assert cloned_query.sql == original_query.sql
    # Assert that the cloned query has the same using
    assert cloned_query.using == original_query.using
    # Assert that the cloned query has the same params
    assert cloned_query.params == original_query.params

    # Assert that the cloned query is a different object
    assert cloned_query is not original_query