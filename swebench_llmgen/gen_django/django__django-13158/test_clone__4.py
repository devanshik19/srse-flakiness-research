import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

def test_clone():
    # Create an initial RawQuery object
    sql = "SELECT * FROM auth_user"
    using = "default"
    params = {'username': 'testuser'}

    original_query = RawQuery(sql, using, params=params)

    # Clone the original RawQuery object
    cloned_query = original_query.clone(using)

    # Assert that the cloned query has the same SQL statement
    assert cloned_query.sql == original_query.sql
    # Assert that the cloned query uses the same parameters
    assert cloned_query.params == original_query.params
    # Assert that the cloned query uses the same 'using' configuration
    assert cloned_query.using == original_query.using

    # Ensure that cloning doesn't affect the original object
    original_query.params['username'] = 'changeduser'
    assert original_query.params['username'] == 'changeduser'
    assert cloned_query.params['username'] == 'testuser'