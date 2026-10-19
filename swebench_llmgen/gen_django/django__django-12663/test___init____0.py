import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.sql.query import RawQuery


def test_raw_query_init():
    sql = "SELECT * FROM auth_user WHERE id = %s"
    using = DEFAULT_DB_ALIAS
    params = (1,)

    raw_query = RawQuery(sql, using, params)

    assert raw_query.sql == sql
    assert raw_query.using == using
    assert raw_query.params == params
    assert raw_query.cursor is None
    assert raw_query.low_mark == 0
    assert raw_query.high_mark is None
    assert isinstance(raw_query.extra_select, dict)
    assert isinstance(raw_query.annotation_select, dict)


def test_raw_query_init_with_empty_params():
    sql = "SELECT * FROM auth_user"
    using = DEFAULT_DB_ALIAS

    raw_query = RawQuery(sql, using)

    assert raw_query.sql == sql
    assert raw_query.using == using
    assert raw_query.params == ()
    assert raw_query.cursor is None
    assert raw_query.low_mark == 0
    assert raw_query.high_mark is None
    assert isinstance(raw_query.extra_select, dict)
    assert isinstance(raw_query.annotation_select, dict)