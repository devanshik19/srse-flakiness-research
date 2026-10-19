import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.sql import compiler
from django.db.models import Lookups

@pytest.mark.parametrize("path, expected_sql", [
    ("$.key", "JSON_EXISTS(%s, 'key')"),
    ("$.nested.key", "JSON_EXISTS(%s, 'nested.key')"),
])
def test_as_oracle(path, expected_sql):
    class TestHasKeyLookup(HasKeyLookup):
        def as_sql(self, compiler, connection, template):
            return f"{template}", [json.dumps({"key": "value"})]

    lookup = TestHasKeyLookup()
    sql, params = lookup.as_oracle(compiler, connection)
    
    assert sql == expected_sql
    assert params == [json.dumps({"key": "value"})]