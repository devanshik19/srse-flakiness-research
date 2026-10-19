import pytest
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.lookups import HasKeyLookup

@pytest.mark.parametrize(
    "json_field, path, expected_sql",
    [
        ('{"key": "value"}', 'key', "JSON_EXISTS(%s, 'key')"),
        ('{"nested": {"key": "value"}}', 'nested.key', "JSON_EXISTS(%s, 'nested.key')"),
        ('{"empty": {}}', 'empty', "JSON_EXISTS(%s, 'empty')"),
    ]
)
def test_as_oracle(json_field, path, expected_sql):
    # Create a User instance for testing
    user = User.objects.create(username='testuser')

    # Create an instance of HasKeyLookup with the parameters required for the test
    lookup = HasKeyLookup()
    compiler = None  # Placeholder; in real tests, a viable compiler object should be passed.
    connection = None  # Placeholder; in real tests, a viable database connection object should be passed.

    # Mock the as_sql method to return the required SQL and parameters
    def mock_as_sql(self, compiler, connection, template):
        return (template % ("sample"), [json_field])

    lookup.as_sql = mock_as_sql.__get__(lookup)

    sql, params = lookup.as_oracle(compiler, connection)
    assert sql == expected_sql % (json_field,)
    assert params == []