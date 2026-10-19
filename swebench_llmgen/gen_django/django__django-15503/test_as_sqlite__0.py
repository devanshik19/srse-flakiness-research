import json
import pytest
from django import forms
from django.core import checks, exceptions
from django.db import NotSupportedError, connections, router
from django.db.models import lookups
from django.db.models.lookups import PostgresOperatorLookup, Transform
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import QuerySet

class HasKeyLookup:
    logical_operator = "AND"

    def as_sql(self, compiler, connection, template):
        return template % ("dummy_field", "dummy_value")

    def as_sqlite(self, compiler, connection):
        return self.as_sql(
            compiler, connection, template="JSON_TYPE(%s, %%s) IS NOT NULL"
        )

@pytest.mark.parametrize("dummy_field, expected_result", [
    ("field_name", "JSON_TYPE(dummy_field, %s) IS NOT NULL"),
])
def test_as_sqlite(dummy_field, expected_result):
    compiler = None  # Replace with actual compiler if needed
    connection = connections['default']
    lookup = HasKeyLookup()
    
    result = lookup.as_sqlite(compiler, connection)
    assert result == expected_result % "dummy_value"