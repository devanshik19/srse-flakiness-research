import pytest
from django.forms import widgets
from django.forms.forms import BaseForm
from django.utils.datastructures import MultiValueDict

class TestBaseForm:
    class DummyWidget(widgets.Widget):
        def value_from_datadict(self, data, files, name):
            return data.get(name)

    def setup_method(self):
        self.form = BaseForm(data=MultiValueDict(), files=MultiValueDict())

    def test_widget_data_value_with_existing_data(self):
        self.form.data = MultiValueDict({'field_name': 'value'})
        widget = self.DummyWidget()
        value = self.form._widget_data_value(widget, 'field_name')
        assert value == 'value'

    def test_widget_data_value_with_no_data(self):
        self.form.data = MultiValueDict()
        widget = self.DummyWidget()
        value = self.form._widget_data_value(widget, 'field_name')
        assert value is None

    def test_widget_data_value_with_multiple_values(self):
        self.form.data = MultiValueDict({'field_name': ['value1', 'value2']})
        widget = self.DummyWidget()
        value = self.form._widget_data_value(widget, 'field_name')
        assert value == ['value1', 'value2']