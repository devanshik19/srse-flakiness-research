import json
import pytest
from django import forms
from django.core import checks, exceptions
from django.db import NotSupportedError, connections
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.fields.json import JSONField
from your_module_path import DataContains  # Adjust with the actual module path

@pytest.mark.parametrize("supports_json, expected", [
    (True, "JSON_CONTAINS(%s, %s)"),
    (False, NotSupportedError),
])
def test_as_sql(supports_json, expected):
    connection = connections['default']
    connection.features.supports_json_field_contains = supports_json
    
    data_contains = DataContains()
    
    if supports_json:
        # Mocking necessary functions
        class Compiler:
            def process_lhs(self, compiler, connection):
                return "lhs", []
            
            def process_rhs(self, compiler, connection):
                return "rhs", []

        compiler = Compiler()
        
        sql, params = data_contains.as_sql(compiler, connection)
        
        assert sql == expected
        assert params == []
    else:
        with pytest.raises(NotSupportedError):
            data_contains.as_sql(None, connection)