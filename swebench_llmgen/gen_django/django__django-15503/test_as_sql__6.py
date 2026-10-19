import pytest
from django.db import connections, NotSupportedError
from django.contrib.auth.models import User
from your_module_path import DataContains  # Update with the actual module path

@pytest.mark.parametrize("supports_json_field_contains, expected_error", [
    (True, None),
    (False, NotSupportedError)
])
def test_as_sql(supports_json_field_contains, expected_error):
    # Arrange
    connection = connections['default']
    connection.features.supports_json_field_contains = supports_json_field_contains
    data_contains_instance = DataContains()

    # Act & Assert
    if expected_error:
        with pytest.raises(expected_error, match="contains lookup is not supported on this database backend."):
            data_contains_instance.as_sql(None, connection)
    else:
        sql, params = data_contains_instance.as_sql(None, connection)
        assert sql == "JSON_CONTAINS(%s, %s)"
        assert params == tuple()  # Adjust according to expected output of process_lhs/process_rhs