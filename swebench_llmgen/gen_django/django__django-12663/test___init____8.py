import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import RawQuery

@pytest.mark.parametrize("sql, using, params, expected_params", [
    ("SELECT * FROM auth_user", "default", None, ()),
    ("SELECT * FROM auth_user WHERE id = %s", "default", (1,), (1,)),
    ("SELECT * FROM auth_user WHERE username = %s", "default", ("test_user",), ("test_user",)),
])
def test_raw_query_init(sql, using, params, expected_params):
    raw_query = RawQuery(sql, using, params)

    assert raw_query.sql == sql
    assert raw_query.using == using
    assert raw_query.params == expected_params
    assert raw_query.low_mark == 0
    assert raw_query.high_mark is None
    assert isinstance(raw_query.extra_select, dict)
    assert isinstance(raw_query.annotation_select, dict)