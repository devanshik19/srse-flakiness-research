import pytest
from django.db.models import F
from django.db.models.fields.json import HasKeyLookup
from django.db import connection

def test_as_oracle():
    # Arrange
    lookup = HasKeyLookup()
    compiler = connection.ops.compiler(connection)
    
    # Simulate necessary inputs
    class MockCompiler:
        def __init__(self):
            self.query = MockQuery()
        
    class MockQuery:
        def __init__(self):
            self.extra_select = {}

    compiler = MockCompiler()
    
    # Act
    sql, params = lookup.as_oracle(compiler, connection)

    # Assert
    assert "JSON_EXISTS" in sql
    assert isinstance(params, list)
    assert len(params) == 0  # Ensure params are as expected