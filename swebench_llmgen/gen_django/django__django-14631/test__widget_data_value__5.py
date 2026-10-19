import pytest
from django.forms import BaseForm, Field, TextInput
from django.utils.datastructures import MultiValueDict

class TestWidgetDataValue:
    class DummyWidget(Field):
        def value_from_datadict(self, data, files, name):
            return data.get(name)

    def test_widget_data_value_with_valid_data(self):
        data = MultiValueDict({'test_field': 'test_value'})
        form = BaseForm(data=data, files=None, auto_id='id_%s', prefix='', initial=None, error_class=None, label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=False, renderer=None)
        widget = self.DummyWidget(widget=TextInput())
        value = form._widget_data_value(widget, 'test_field')
        assert value == 'test_value'

    def test_widget_data_value_with_no_data(self):
        data = MultiValueDict({})
        form = BaseForm(data=data, files=None, auto_id='id_%s', prefix='', initial=None, error_class=None, label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=False, renderer=None)
        widget = self.DummyWidget(widget=TextInput())
        value = form._widget_data_value(widget, 'test_field')
        assert value is None

    def test_widget_data_value_with_empty_string(self):
        data = MultiValueDict({'test_field': ''})
        form = BaseForm(data=data, files=None, auto_id='id_%s', prefix='', initial=None, error_class=None, label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=False, renderer=None)
        widget = self.DummyWidget(widget=TextInput())
        value = form._widget_data_value(widget, 'test_field')
        assert value == ''