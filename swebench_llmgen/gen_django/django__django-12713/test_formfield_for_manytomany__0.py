import pytest
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.db import models
from django.forms.models import ManyToManyField
from django.utils.text import format_lazy


class TestModel(models.Model):
    users = ManyToManyField(User, related_name='test_models', blank=True)


class TestAdmin(BaseModelAdmin):
    autocomplete_fields = ['users']
    raw_id_fields = []
    filter_vertical = []
    filter_horizontal = []


@pytest.fixture
def test_admin():
    return TestAdmin()


@pytest.fixture
def test_model():
    return TestModel.objects.create()


def test_formfield_for_manytomany_with_autocomplete(test_admin, test_model):
    db_field = TestModel._meta.get_field('users')
    request = None  # Simulate request context as needed
    form_field = test_admin.formfield_for_manytomany(db_field, request)

    assert isinstance(form_field.widget, widgets.AutocompleteSelectMultiple)
    assert 'queryset' in form_field._kwargs


def test_formfield_for_manytomany_with_raw_id(test_admin, test_model):
    test_admin.raw_id_fields = ['users']
    db_field = TestModel._meta.get_field('users')
    request = None  # Simulate request context as needed
    form_field = test_admin.formfield_for_manytomany(db_field, request)

    assert isinstance(form_field.widget, widgets.ManyToManyRawIdWidget)


def test_formfield_for_manytomany_with_filtered_select(test_admin, test_model):
    test_admin.filter_horizontal = ['users']
    db_field = TestModel._meta.get_field('users')
    request = None  # Simulate request context as needed
    form_field = test_admin.formfield_for_manytomany(db_field, request)

    assert isinstance(form_field.widget, widgets.FilteredSelectMultiple)


def test_formfield_for_manytomany_no_intermediary(test_admin):
    class IntermediaryModel(models.Model):
        # Simulating a non-auto created intermediary model
        test_models = models.ManyToManyField(TestModel)

    db_field = IntermediaryModel._meta.get_field('test_models')
    request = None
    form_field = test_admin.formfield_for_manytomany(db_field, request)

    assert form_field is None


def test_formfield_for_manytomany_with_help_text(test_admin):
    db_field = TestModel._meta.get_field('users')
    request = None  # Simulate request context as needed
    form_field = test_admin.formfield_for_manytomany(db_field, request)

    form_field.help_text = None
    form_field = test_admin.formfield_for_manytomany(db_field, request)

    assert form_field.help_text == format_lazy(
        _('Hold down “Control”, or “Command” on a Mac, to select more than one.'))