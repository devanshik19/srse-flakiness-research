import pytest
from django.db.models.fields.json import HasKeyLookup
from django.contrib.auth.models import User

@pytest.mark.parametrize("path_expression, expected_sql", [
    ("$.key", "JSON_EXISTS(%s, '%s')"),
    ("$.another_key", "JSON_EXISTS(%s, '%s')")
])
def test_as_oracle(path_expression, expected_sql):
    # Arrange
    compiler = None  # Dummy value, as we do not need a real compiler for this test
    connection = None  # Dummy value, as we do not need a real connection for this test
    
    lookup = HasKeyLookup()
    
    # Mocking the as_sql method to return required values for testing as_oracle
    lookup.as_sql = lambda comp, conn, template: (template, [path_expression])

    # Act
    sql, params = lookup.as_oracle(compiler, connection)

    # Assert
    assert sql == expected_sql % (None, path_expression)
    assert params == []