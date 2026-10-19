import pytest
from django.contrib.auth.models import User
from django.db.models import FloatField
from django.db import connection, NotSupportedError

class DataContains:
    def as_sql(self, compiler, connection):
        if not connection.features.supports_json_field_contains:
            raise NotSupportedError(
                "contains lookup is not supported on this database backend."
            )
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = tuple(lhs_params) + tuple(rhs_params)
        return "JSON_CONTAINS(%s, %s)" % (lhs, rhs), params
    
    # Mocked methods for testing purposes
    def process_lhs(self, compiler, connection):
        return 'json_field', ['{"key": "value"}']  # Example LHS
    
    def process_rhs(self, compiler, connection):
        return '"value"', []  # Example RHS

def test_as_sql_supports_json_field_contains():
    connection.features.supports_json_field_contains = True
    field = DataContains()
    compiler = None  # Assuming compiler is not needed for this test

    sql, params = field.as_sql(compiler, connection)
    
    assert sql == "JSON_CONTAINS(json_field, \"value\")"
    assert params == ({"key": "value"},)

def test_as_sql_not_supported():
    connection.features.supports_json_field_contains = False
    field = DataContains()
    compiler = None  # Assuming compiler is not needed for this test

    with pytest.raises(NotSupportedError, match="contains lookup is not supported on this database backend."):
        field.as_sql(compiler, connection)