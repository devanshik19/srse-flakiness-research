import json
import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.fields.json import HasKeyLookup

@pytest.mark.parametrize("json_data, key_path, expected_sql", [
    ({"name": "John", "details": {"age": 30}}, 'details.age', "JSON_EXISTS(%s, 'details.age')"),
    ({"name": "Jane"}, 'details', "JSON_EXISTS(%s, 'details')"),
])
def test_as_oracle(json_data, key_path, expected_sql):
    # Arrange
    user = User.objects.create(username='testuser', email='test@example.com', password='password')

    # Act
    lookup = HasKeyLookup()
    lookup._key = key_path
    compiler = lookup.as_sql  # Using the as_sql method to simulate SQL generation
    
    # Mocking the compiler and connection as we only want to test `as_oracle`
    class MockCompiler:
        pass

    class MockConnection:
        pass

    mock_compiler = MockCompiler()
    mock_connection = MockConnection()

    sql, params = lookup.as_oracle(mock_compiler, mock_connection)

    # Assert
    assert sql == expected_sql % (json.dumps(json_data),)
    assert params == []