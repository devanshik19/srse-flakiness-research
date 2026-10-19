import json
import pytest
from django.db import connections
from django.contrib.auth.models import User
from django.db.models import Lookup

class HasKeyLookup(Lookup):
    def as_sql(self, compiler, connection, template):
        # Simulate the implementation of as_sql
        sql = "SELECT * FROM my_table WHERE JSON_EXISTS(my_field, %s)"
        return sql, [self.rhs]

    def as_oracle(self, compiler, connection):
        sql, params = self.as_sql(compiler, connection, template="JSON_EXISTS(%s, '%%s')")
        return sql % tuple(params), []

@pytest.mark.parametrize("path, expected_sql", [
    ("$.key", "SELECT * FROM my_table WHERE JSON_EXISTS(my_field, '%.key')"),
    ("$.another_key", "SELECT * FROM my_table WHERE JSON_EXISTS(my_field, '%.another_key')"),
])
def test_as_oracle(path, expected_sql):
    user = User.objects.create_user(username='testuser', password='testpass')
    lookup = HasKeyLookup(lhs='my_field', rhs=path)
    
    sql, _ = lookup.as_oracle(None, connections['default'])
    
    assert sql.strip() == expected_sql.strip()