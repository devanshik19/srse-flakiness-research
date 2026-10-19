import json
import pytest
from django import forms
from django.core import checks, exceptions
from django.db import NotSupportedError, connections, router
from django.db.models import lookups
from django.db.models.lookups import PostgresOperatorLookup, Transform
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

class DataContains:
    lookup_name = 'contains'
    postgres_operator = PostgresOperatorLookup

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
        # Dummy implementation for the sake of the test
        return 'lhs_field', []

    def process_rhs(self, compiler, connection):
        # Dummy implementation for the sake of the test
        return 'rhs_field', []

@pytest.mark.django_db
def test_as_sql_contains_lookup():
    user = User.objects.create_user(username='testuser', password='testpass')
    connection = connections[router.db_for_write(User)]
    
    # Test when JSON contains is supported
    if connection.features.supports_json_field_contains:
        data_contains = DataContains()

        sql, params = data_contains.as_sql(None, connection)

        assert sql == "JSON_CONTAINS(lhs_field, rhs_field)"
        assert params == []

    # Test when JSON contains is not supported
    connection.features.supports_json_field_contains = False
    data_contains = DataContains()

    with pytest.raises(NotSupportedError) as excinfo:
        data_contains.as_sql(None, connection)
    
    assert str(excinfo.value) == "contains lookup is not supported on this database backend."