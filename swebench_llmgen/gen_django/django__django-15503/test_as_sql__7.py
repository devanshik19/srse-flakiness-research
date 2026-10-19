import pytest
from django.db import NotSupportedError
from django.db.models import Func, F
from django.contrib.auth.models import User
from django.db import connection

class DataContains(Func):
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
def test_as_sql(supports_json):
    # Set up the connection features for the test
    connection.features.supports_json_field_contains = supports_json
    data_contains = DataContains(F('field_name'), 'value')  # Assuming the field exists

    if supports_json:
        sql, params = data_contains.as_sql(None, connection)
        assert sql == "JSON_CONTAINS(%s, %s)" % ('field_name', 'value')
        assert params == ('field_name', 'value')
    else:
        with pytest.raises(NotSupportedError, match="contains lookup is not supported on this database backend."):
            data_contains.as_sql(None, connection)