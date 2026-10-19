import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.query import RawQuery

def test_raw_query_init():
    sql = "SELECT * FROM auth_user WHERE username = %s"
    using = connection
    params = ('testuser',)

    raw_query = RawQuery(sql, using, params)

    assert raw_query.sql == sql
    assert raw_query.using == using
    assert raw_query.params == params
    assert raw_query.cursor is None
    assert raw_query.low_mark == 0
    assert raw_query.high_mark is None
    assert raw_query.extra_select == {}
    assert raw_query.annotation_select == {}

    # Test with no params
    raw_query_no_params = RawQuery(sql, using)

    assert raw_query_no_params.params == ()