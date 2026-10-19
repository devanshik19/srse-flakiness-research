import pytest
from django.forms import BaseForm
from django.contrib.auth.models import User

class TestBaseForm(BaseForm):
    def __init__(self, data=None, initial=None):
        self.data = MultiValueDict(data or {})
        self.initial = initial or {}
        self.changed_data = []
        super().__init__(data=self.data, files=None, auto_id=None, prefix=None,
                         initial=self.initial, error_class=None,
                         label_suffix=':', empty_permitted=False,
                         field_order=None, use_required_attribute=False,
                         renderer=None)

def test_has_changed_no_initial_data():
    form = TestBaseForm(data={'field1': 'value1'}, initial={})
    assert not form.has_changed()

def test_has_changed_with_initial_data_no_change():
    form = TestBaseForm(data={'field1': 'value1'}, initial={'field1': 'value1'})
    assert not form.has_changed()

def test_has_changed_with_initial_data_change():
    form = TestBaseForm(data={'field1': 'new_value'}, initial={'field1': 'value1'})
    form.changed_data.append('field1')
    assert form.has_changed()

def test_has_changed_with_multiple_fields():
    form = TestBaseForm(data={'field1': 'value1', 'field2': 'value2'},
                        initial={'field1': 'value1', 'field2': 'value2'})
    assert not form.has_changed()
    
    form.data['field2'] = 'new_value'
    form.changed_data.append('field2')
    assert form.has_changed()

def test_has_changed_multiple_changes():
    form = TestBaseForm(data={'field1': 'changed_value1', 'field2': 'changed_value2'},
                        initial={'field1': 'original_value1', 'field2': 'original_value2'})
    form.changed_data.extend(['field1', 'field2'])
    assert form.has_changed()