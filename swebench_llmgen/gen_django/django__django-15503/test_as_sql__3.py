import pytest
from django.db import connection
from django.db.models import F
from django.contrib.auth.models import User
from django.core.exceptions import NotSupportedError
from .fields.json import DataContains

@pytest.mark.django_db
def test_as_sql_unsupported_database():
    # Mocking a connection that does not support JSON field contains
    connection.features.supports_json_field_contains = False
    data_contains = DataContains()

    with pytest.raises(NotSupportedError, match="contains lookup is not supported on this database backend."):
        data_contains.as_sql(None, connection)

@pytest.mark.django_db
def test_as_sql_supported_database():
    # Setup a valid connection that supports JSON field contains
    connection.features.supports_json_field_contains = True
    data_contains = DataContains()
    compiler = None  # Replace with actual compiler mock if needed

    # Simulating the process_lhs and process_rhs methods
    data_contains.process_lhs = lambda compiler, connection: ("json_field", [])
    data_contains.process_rhs = lambda compiler, connection: ('"value"', [])

    sql, params = data_contains.as_sql(compiler, connection)
    assert sql == "JSON_CONTAINS(%s, %s)"
    assert params == ("json_field", '"value"')