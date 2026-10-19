import pytest
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:

    def test_init_required_false(self):
        field = ReadOnlyPasswordHashField()
        assert field.required is False

    def test_init_required_true(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required is True

    def test_init_with_custom_args(self):
        field = ReadOnlyPasswordHashField(label='Custom Label', initial='initial_value')
        assert field.label == 'Custom Label'
        assert field.initial == 'initial_value'
        assert field.required is False