import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.sql.query import RawQuery

def test_raw_query_init_with_params():
    sql = "SELECT * FROM auth_user WHERE id = %s"
    using = DEFAULT_DB_ALIAS
    params = (1,)

    query = RawQuery(sql, using, params)

    assert query.sql == sql
    assert query.using == using
    assert query.params == params
    assert query.low_mark == 0
    assert query.high_mark is None
    assert query.extra_select == {}
    assert query.annotation_select == {}

def test_raw_query_init_without_params():
    sql = "SELECT * FROM auth_user"
    using = DEFAULT_DB_ALIAS

    query = RawQuery(sql, using)

    assert query.sql == sql
    assert query.using == using
    assert query.params == ()
    assert query.low_mark == 0
    assert query.high_mark is None
    assert query.extra_select == {}
    assert query.annotation_select == {}