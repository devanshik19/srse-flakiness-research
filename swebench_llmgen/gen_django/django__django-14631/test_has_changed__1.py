import copy
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms.fields import Field, FileField
from django.forms.utils import ErrorDict, ErrorList
from django.forms.widgets import Media, MediaDefiningClass
from django.utils.datastructures import MultiValueDict
from django.utils.functional import cached_property
from django.utils.html import conditional_escape, html_safe
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django import forms
from django.contrib.auth.models import User
import pytest

class TestBaseForm(forms.BaseForm):
    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.changed_data = []

    def clean(self):
        if self.data.get('name'):
            self.changed_data.append('name')

class TestHasChanged:
    def test_has_changed_no_initial_data(self):
        form = TestBaseForm(data={})
        assert not form.has_changed()

    def test_has_changed_with_initial_data(self):
        form = TestBaseForm(data={'name': 'John'})
        form.changed_data.append('name')
        assert form.has_changed()

    def test_has_changed_with_different_data(self):
        form = TestBaseForm(data={'name': 'Jane'})
        form.changed_data.append('name')
        assert form.has_changed()

    def test_has_changed_after_reset(self):
        form = TestBaseForm(data={'name': 'John'})
        form.changed_data.append('name')
        assert form.has_changed()

        # Simulate a reset of changed_data
        form.changed_data = []
        assert not form.has_changed()

        # Adding a new change
        form.changed_data.append('new_name')
        assert form.has_changed()