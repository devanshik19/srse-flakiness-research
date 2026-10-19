import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.sql.query import RawQuery

@pytest.mark.parametrize("sql, using, params", [
    ("SELECT * FROM auth_user", DEFAULT_DB_ALIAS, None),
    ("SELECT * FROM auth_user WHERE username = %s", DEFAULT_DB_ALIAS, ("testuser",)),
    ("SELECT * FROM auth_user LIMIT 10", DEFAULT_DB_ALIAS, ()),
])
def test_raw_query_init(sql, using, params):
    raw_query = RawQuery(sql, using, params)

    assert raw_query.sql == sql
    assert raw_query.using == using
    assert raw_query.params == (params or ())
    assert raw_query.low_mark == 0
    assert raw_query.high_mark is None
    assert raw_query.extra_select == {}
    assert raw_query.annotation_select == {}