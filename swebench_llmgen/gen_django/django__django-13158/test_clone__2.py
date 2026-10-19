import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

@pytest.fixture
def raw_query():
    sql = "SELECT * FROM auth_user WHERE username = %s"
    using = "default"
    params = ["testuser"]
    return RawQuery(sql, using, params=params)

def test_clone(raw_query):
    cloned_query = raw_query.clone(using="custom_db")

    # Verify that the SQL is copied correctly
    assert cloned_query.sql == raw_query.sql
    # Ensure params are copied correctly
    assert cloned_query.params == raw_query.params
    # Check that the using database is correctly set in the clone
    assert cloned_query.using == "custom_db"