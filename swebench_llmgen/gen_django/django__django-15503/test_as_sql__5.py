import json
import pytest
from django.contrib.auth.models import User
from django.db import NotSupportedError, connections
from django.db.models import Field

class DataContains(Field):

    def as_sql(self, compiler, connection):
        if not connection.features.supports_json_field_contains:
            raise NotSupportedError(
                "contains lookup is not supported on this database backend."
            )
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = tuple(lhs_params) + tuple(rhs_params)
        return "JSON_CONTAINS(%s, %s)" % (lhs, rhs), params

@pytest.mark.parametrize("supports_json", [True, False])
def test_as_sql(monkeypatch, supports_json):
    class MockConnection:
        features = type('features', (), {"supports_json_field_contains": supports_json})

    class MockCompiler:
        def __init__(self, connection):
            self.connection = connection

    monkeypatch.setattr(connections, 'get_unusable', lambda: MockConnection())

    data_contains = DataContains()
    compiler = MockCompiler(MockConnection())

    if supports_json:
        # Simulate process_lhs and process_rhs methods for testing purposes.
        data_contains.process_lhs = lambda c, conn: ("lhs_value", [])
        data_contains.process_rhs = lambda c, conn: ("rhs_value", [])
        
        sql, params = data_contains.as_sql(compiler, compiler.connection)
        assert sql == "JSON_CONTAINS(lhs_value, rhs_value)"
        assert params == []
    else:
        with pytest.raises(NotSupportedError, match="contains lookup is not supported on this database backend."):
            data_contains.as_sql(compiler, compiler.connection)