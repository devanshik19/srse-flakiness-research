import pytest
from django.core.exceptions import NotSupportedError
from django.db import connections
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.fields.json import DataContains

def test_as_sql_with_supported_connection():
    class MockCompiler:
        def __init__(self):
            self.query = {}

    connection = connections.databases['default']
    connection.features.supports_json_field_contains = True  # Simulating supported feature

    lookup = DataContains()

    # Assume necessary processing methods return certain values
    lookup.process_lhs = lambda compiler, connection: ("lhs_json_field", [])
    lookup.process_rhs = lambda compiler, connection: ("rhs_value", [])

    sql, params = lookup.as_sql(MockCompiler(), connection)
    assert sql == "JSON_CONTAINS(lhs_json_field, rhs_value)"
    assert params == []

def test_as_sql_with_unsupported_connection():
    class MockCompiler:
        def __init__(self):
            self.query = {}

    connection = connections.databases['default']
    connection.features.supports_json_field_contains = False  # Simulating unsupported feature

    lookup = DataContains()

    with pytest.raises(NotSupportedError, match="contains lookup is not supported on this database backend."):
        lookup.as_sql(MockCompiler(), connection)