import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class TestField:

    def test_get_db_prep_value_without_prepared(self):
        field = Field()
        value = 'Sample Value'
        connection = User._state.db  # Use the default database connection
        prepared = False
        
        result = field.get_db_prep_value(value, connection, prepared)
        
        assert result == field.get_prep_value(value)

    def test_get_db_prep_value_with_prepared(self):
        field = Field()
        value = 'Sample Value'
        connection = User._state.db  # Use the default database connection
        prepared = True
        
        result = field.get_db_prep_value(value, connection, prepared)
        
        assert result == value