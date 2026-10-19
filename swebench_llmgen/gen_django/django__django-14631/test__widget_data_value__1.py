import pytest
from django import forms
from django.forms.widgets import TextInput
from django.utils.datastructures import MultiValueDict

class DummyWidget(TextInput):
    def value_from_datadict(self, data, files, name):
        return data.get(name, '')

class TestBaseForm:
    @pytest.fixture
    def form(self):
        class SampleForm(forms.BaseForm):
            field = forms.CharField(widget=DummyWidget())

        return SampleForm(data={'field': 'test_value'}, files=MultiValueDict())

    def test_widget_data_value(self, form):
        widget = form.fields['field'].widget
        value = form._widget_data_value(widget, 'field')
        assert value == 'test_value'

    def test_widget_data_value_missing(self, form):
        form_with_missing_data = form.__class__(data={}, files=MultiValueDict())
        widget = form_with_missing_data.fields['field'].widget
        value = form_with_missing_data._widget_data_value(widget, 'field')
        assert value == ''