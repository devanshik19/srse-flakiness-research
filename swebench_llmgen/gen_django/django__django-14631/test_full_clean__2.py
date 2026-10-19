import pytest
from django.forms import BaseForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class TestBaseForm(BaseForm):

    def __init__(self, *args, **kwargs):
        self.data = kwargs.pop('data', None)
        self.fields = {}
        super().__init__(*args, **kwargs)
    
    def _clean_fields(self):
        # Simulate field cleaning
        for field_name in self.fields:
            if field_name in self.data:
                if not self.data[field_name]:
                    self.add_error(field_name, 'This field is required.')

    def _clean_form(self):
        # Simulate form cleaning logic
        pass

    def _post_clean(self):
        # Simulate post clean logic
        pass

@pytest.mark.parametrize("data, is_bound, empty_permitted, expected_errors", [
    ({"name": "John"}, True, False, {}),
    ({"name": ""}, True, False, {'name': ['This field is required.']}),
    ({}, True, True, {}),
    ({"name": "John"}, False, False, {}),
])
def test_full_clean(data, is_bound, empty_permitted, expected_errors):
    form = TestBaseForm(data=data, empty_permitted=empty_permitted)
    form.is_bound = is_bound
    form.fields['name'] = 'name'  # Add a field to be cleaned

    form.full_clean()

    assert form.errors.get('name') == expected_errors.get('name')
    if expected_errors:
        assert len(form._errors) > 0
    else:
        assert not form._errors