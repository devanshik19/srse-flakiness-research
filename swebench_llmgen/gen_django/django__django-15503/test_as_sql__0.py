import pytest
from django.db import connections, NotSupportedError
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.db import models

class DataContains:
    lookup_name = 'contains'
    
    def as_sql(self, compiler, connection):
        if not connection.features.supports_json_field_contains:
            raise NotSupportedError(
                "contains lookup is not supported on this database backend."
            )
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = tuple(lhs_params) + tuple(rhs_params)
        return "JSON_CONTAINS(%s, %s)" % (lhs, rhs), params

    def process_lhs(self, compiler, connection):
        # Simulating LHS processing for demonstration
        return 'some_lhs', []
    
    def process_rhs(self, compiler, connection):
        # Simulating RHS processing for demonstration
        return 'some_rhs', []

@pytest.mark.parametrize('supports_json_field_contains, expected', [
    (True, "JSON_CONTAINS(%s, %s)"),
    (False, NotSupportedError),
])
def test_data_contains_as_sql(supports_json_field_contains, expected):
    class TestModel(models.Model):
        data = JSONField()
    
    # Patch the connection feature for testing
    connection = connections['default']
    original_support = connection.features.supports_json_field_contains
    connection.features.supports_json_field_contains = supports_json_field_contains

    data_contains = DataContains()
    
    if supports_json_field_contains:
        sql, params = data_contains.as_sql(None, connection)
        assert sql == expected % ('some_lhs', 'some_rhs')
        assert params == []
    else:
        with pytest.raises(NotSupportedError):
            data_contains.as_sql(None, connection)

    # Restore original feature value to avoid side effects
    connection.features.supports_json_field_contains = original_support