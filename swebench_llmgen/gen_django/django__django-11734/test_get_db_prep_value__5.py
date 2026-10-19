import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class TestFieldGetDbPrepValue:

    def test_get_db_prep_value_not_prepared(self):
        field = Field()
        value = "test_value"
        connection = None  # Mock connection if necessary
        prepared = False
        
        # Simulating the `get_prep_value` method
        field.get_prep_value = lambda v: f"prepared_{v}"
        
        result = field.get_db_prep_value(value, connection, prepared)
        
        assert result == "prepared_test_value"

    def test_get_db_prep_value_prepared(self):
        field = Field()
        value = "test_value"
        connection = None  # Mock connection if necessary
        prepared = True
        
        result = field.get_db_prep_value(value, connection, prepared)
        
        assert result == "test_value"