import pytest
from django import forms

class TestField:
    @pytest.fixture
    def field_instance(self):
        class TestField(forms.Field):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        return TestField()

    def test_bound_data_when_disabled(self, field_instance):
        field_instance.disabled = True
        initial = "Initial Value"
        data = "Submitted Value"
        assert field_instance.bound_data(data, initial) == initial

    def test_bound_data_when_not_disabled(self, field_instance):
        field_instance.disabled = False
        initial = "Initial Value"
        data = "Submitted Value"
        assert field_instance.bound_data(data, initial) == data