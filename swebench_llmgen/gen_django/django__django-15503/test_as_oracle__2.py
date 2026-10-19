import pytest
from django.db.models import Func
from django.db.models import ExpressionWrapper, F
from django.contrib.auth.models import User

class HasKeyLookup(Func):
    def as_sql(self, compiler, connection, template):
        # Simple SQL emulation for demonstration purposes
        return "SELECT * FROM my_table WHERE my_json_field IS NOT NULL", []

    def as_oracle(self, compiler, connection):
        sql, params = self.as_sql(
            compiler, connection, template="JSON_EXISTS(%s, '%%s')"
        )
        return sql % tuple(params), []

@pytest.mark.parametrize("json_field, expected_sql", [
    ({"key": "value"}, "SELECT * FROM my_table WHERE my_json_field IS NOT NULL"),
])
def test_as_oracle(expected_sql, json_field):
    user = User.objects.create(username='testuser', password='testpass')

    # Assuming we attach a JSON field to the user model or testing with a function
    has_key_lookup = HasKeyLookup(F('my_json_field'))

    # Simulating a mock compiler and connection
    class MockCompiler:
        pass

    class MockConnection:
        pass

    compiler = MockCompiler()
    connection = MockConnection()

    sql, params = has_key_lookup.as_oracle(compiler, connection)
    assert sql.strip() == expected_sql.strip()
    assert params == []