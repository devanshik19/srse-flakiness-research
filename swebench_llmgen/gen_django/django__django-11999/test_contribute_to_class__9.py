import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class TestField:
    def test_contribute_to_class(self):
        # Create a custom field instance
        field = Field()

        # Create a class (model) to contribute to
        class TestModel:
            _meta = type('Meta', (object,), {'fields': []})
            attname = 'test_field'
            descriptor_class = lambda self, field: field  # Simple descriptor mock

            @classmethod
            def _get_FIELD_display(cls, field):
                return f"Field display for {field.attname}"

        # Contribute the field to the TestModel class
        field.contribute_to_class(TestModel, 'test_field')

        # Check that the field was added to the meta fields
        assert field in TestModel._meta.fields

        # Check that the attribute was set correctly
        assert hasattr(TestModel, 'test_field')
        assert isinstance(getattr(TestModel, 'test_field'), Field)

        # Check the display method was set
        assert hasattr(TestModel, 'get_test_field_display')
        display_method = TestModel.get_test_field_display
        assert display_method() == "Field display for test_field"

        # Contribute with private_only=True
        field2 = Field()
        field2.contribute_to_class(TestModel, 'private_test_field', private_only=True)

        # Check that the field was added to the meta fields as private
        assert field2 in TestModel._meta.fields

        # Since private_only, the attribute should not be accessible directly
        assert not hasattr(TestModel, 'private_test_field')