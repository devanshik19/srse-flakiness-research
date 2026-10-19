import pytest
from django.forms import fields
from django.contrib.auth.models import User

class TestField:

    @pytest.fixture
    def field_instance(self):
        return fields.Field()

    def test_deepcopy_with_valid_data(self, field_instance):
        original_widget = field_instance.widget
        original_validators = field_instance.validators
        copied_field = field_instance.__deepcopy__({})

        assert copied_field is not field_instance
        assert copied_field.widget is not original_widget
        assert copied_field.validators == original_validators

    def test_deepcopy_memoization(self, field_instance):
        memo = {}
        copied_field_1 = field_instance.__deepcopy__(memo)
        copied_field_2 = field_instance.__deepcopy__(memo)

        assert copied_field_1 is not copied_field_2
        assert copied_field_1 in memo.values()
        assert copied_field_2 in memo.values()
        assert len(memo) == 1  # Only one instance should be stored in memo

    def test_deepcopy_widget(self, field_instance):
        original_widget = field_instance.widget
        # Modify the widget to see if deepcopy is working
        field_instance.widget = fields.TextInput()
        copied_field = field_instance.__deepcopy__({})
        
        assert copied_field.widget is not field_instance.widget
        assert isinstance(copied_field.widget, fields.TextInput)