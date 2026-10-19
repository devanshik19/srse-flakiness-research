import pytest
from django.contrib.auth.models import User
from django.db.models import Field


class TestField:

    @pytest.fixture
    def field_instance(self):
        return Field()

    def test_get_db_prep_value_not_prepared(self, field_instance):
        value = 'Sample Value'
        connection = None  # As direct DB interaction is not necessary for this test
        
        # Mocking get_prep_value method on the Field instance
        field_instance.get_prep_value = lambda val: f'Prepared {val}'
        
        result = field_instance.get_db_prep_value(value, connection, prepared=False)
        assert result == 'Prepared Sample Value'

    def test_get_db_prep_value_prepared(self, field_instance):
        value = 'Sample Value'
        connection = None  # As direct DB interaction is not necessary for this test
        
        result = field_instance.get_db_prep_value(value, connection, prepared=True)
        assert result == value