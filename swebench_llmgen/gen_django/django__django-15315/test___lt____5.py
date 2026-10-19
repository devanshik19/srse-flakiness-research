import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class TestFieldComparison:
    def test_lt_creation_counter(self):
        field1 = Field()
        field1.creation_counter = 1
        field2 = Field()
        field2.creation_counter = 2
        
        assert field1 < field2

    def test_lt_creation_counter_reverse(self):
        field1 = Field()
        field1.creation_counter = 2
        field2 = Field()
        field2.creation_counter = 1
        
        assert not (field1 < field2)

    def test_lt_creation_counter_equal_no_model(self):
        field1 = Field()
        field1.creation_counter = 1
        field2 = Field()
        field2.creation_counter = 1
        field1.model = None
        field2.model = None
        
        assert not (field1 < field2)

    def test_lt_creation_counter_equal_field_model(self):
        field1 = Field()
        field1.creation_counter = 1
        field1.model = User
        
        field2 = Field()
        field2.creation_counter = 1
        field2.model = User
        
        assert not (field1 < field2)

    def test_lt_different_models(self):
        field1 = Field()
        field1.creation_counter = 1
        field1.model = User
        
        field2 = Field()
        field2.creation_counter = 1
        field2.model = None
        
        assert field2 < field1

    def test_lt_diff_models_app_label_comparison(self):
        field1 = Field()
        field1.creation_counter = 1
        field1.model = User  # Assume User has a certain app_label and model_name
        
        field2 = Field()
        field2.creation_counter = 1
        # Creating a mock model class for the comparison.
        class OtherModel:
            _meta = type('Meta', (), {
                'app_label': 'other_app',
                'model_name': 'other_model'
            })

        field2.model = OtherModel
        
        assert field1 < field2