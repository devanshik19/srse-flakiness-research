import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

class TestModel(models.Model):
    users = models.ManyToManyField(User)

class TestModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['users']
    raw_id_fields = []
    filter_vertical = []
    filter_horizontal = []

@pytest.fixture
def test_model_admin():
    return TestModelAdmin(TestModel, admin.site)

def test_formfield_for_manytomany_with_autocomplete(test_model_admin):
    db_field = TestModel._meta.get_field('users')
    request = None
    form_field = test_model_admin.formfield_for_manytomany(db_field, request)

    assert isinstance(form_field.widget, admin.widgets.AutocompleteSelectMultiple)
    assert form_field.queryset.model == User._meta.model

def test_formfield_for_manytomany_with_raw_id(test_model_admin):
    test_model_admin.raw_id_fields = ['users']
    db_field = TestModel._meta.get_field('users')
    request = None
    form_field = test_model_admin.formfield_for_manytomany(db_field, request)

    assert isinstance(form_field.widget, admin.widgets.ManyToManyRawIdWidget)

def test_formfield_for_manytomany_with_filtered_select(test_model_admin):
    test_model_admin.filter_horizontal = ['users']
    db_field = TestModel._meta.get_field('users')
    request = None
    form_field = test_model_admin.formfield_for_manytomany(db_field, request)

    assert isinstance(form_field.widget, admin.widgets.FilteredSelectMultiple)

def test_formfield_for_manytomany_no_queryset(test_model_admin):
    db_field = TestModel._meta.get_field('users')
    request = None
    form_field = test_model_admin.formfield_for_manytomany(db_field, request)

    assert 'queryset' in form_field.__dict__

def test_formfield_for_manytomany_without_intermediary(test_model_admin):
    class NonAutoCreatedIntermediaryModel(models.Model):
        pass

    db_field = NonAutoCreatedIntermediaryModel._meta.get_field('users')
    request = None
    result = test_model_admin.formfield_for_manytomany(db_field, request)

    assert result is None