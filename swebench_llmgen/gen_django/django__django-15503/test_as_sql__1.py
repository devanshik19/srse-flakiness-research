import pytest
from django.db import NotSupportedError, connections
from django.contrib.auth.models import User
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

    # Placeholder for other methods
    def process_lhs(self, compiler, connection):
        return 'lhs_field', ['lhs_param']

    def process_rhs(self, compiler, connection):
        return 'rhs_field', ['rhs_param']


def test_as_sql_supports_json_field_contains(connection):
    # This test checks the case where the database supports JSON field contains.
    connection.features.supports_json_field_contains = True
    data_contains = DataContains()

    sql, params = data_contains.as_sql(None, connection)

    assert sql == "JSON_CONTAINS(lhs_field, rhs_field)"
    assert params == ('lhs_param', 'rhs_param')


def test_as_sql_does_not_support_json_field_contains(connection):
    # This test checks the case where the database does not support JSON field contains.
    connection.features.supports_json_field_contains = False
    data_contains = DataContains()

    with pytest.raises(NotSupportedError, match="contains lookup is not supported on this database backend."):
        data_contains.as_sql(None, connection)