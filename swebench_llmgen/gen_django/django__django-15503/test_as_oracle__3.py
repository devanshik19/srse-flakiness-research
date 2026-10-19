import pytest
from django.contrib.auth.models import User
from django.db.models import Expressions
from django.db.models.fields.json import HasKeyLookup

class DummyCompiler:
    def __init__(self):
        self.query = None

class DummyConnection:
    pass

def test_as_oracle():
    # Create an instance of the HasKeyLookup with test parameters
    lookup = HasKeyLookup()

    # Mocking the compiler and connection
    compiler = DummyCompiler()
    connection = DummyConnection()

    # Create the necessary structure for as_sql method call
    compiler.query = Expressions()
    
    # Mock output of as_sql; depending on your actual implementation, you might have to adjust
    def mock_as_sql(compiler, connection, template):
        return "SELECT * FROM table WHERE JSON_EXISTS(data, '%s')", ['key']
    
    # Assign the mock method to the lookup instance
    lookup.as_sql = mock_as_sql

    # Call the as_oracle function
    sql, params = lookup.as_oracle(compiler, connection)

    # Validate the returned SQL statement and params
    assert sql == "SELECT * FROM table WHERE JSON_EXISTS(data, 'key')"
    assert params == []