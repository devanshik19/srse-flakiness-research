import pytest
from django import forms
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

    def get_field_queryset(self, using, db_field, request):
        if db_field.name == 'users':
            return User.objects.all()
        return super().get_field_queryset(using, db_field, request)

    def get_autocomplete_fields(self, request):
        return self.autocomplete_fields

def test_formfield_for_manytomany():
    admin_site = admin.site
    model_admin = TestModelAdmin(TestModel, admin_site)

    db_field = TestModel._meta.get_field('users')
    request = None  # Assuming no specific request object is needed for this test
    kwargs = {}

    # Test with autocomplete fields
    form_field = model_admin.formfield_for_manytomany(db_field, request, **kwargs)
    assert isinstance(form_field.widget, admin.widgets.AutocompleteSelectMultiple)
    assert 'queryset' in kwargs

    # Test with raw_id_fields
    model_admin.raw_id_fields = ['users']
    form_field = model_admin.formfield_for_manytomany(db_field, request, **kwargs)
    assert isinstance(form_field.widget, admin.widgets.ManyToManyRawIdWidget)

    # Test with filter_vertical
    model_admin.filter_vertical = ['users']
    form_field = model_admin.formfield_for_manytomany(db_field, request, **kwargs)
    assert isinstance(form_field.widget, admin.widgets.FilteredSelectMultiple)

    # Test with no specific fields
    model_admin.autocomplete_fields = []
    model_admin.raw_id_fields = []
    model_admin.filter_vertical = []
    form_field = model_admin.formfield_for_manytomany(db_field, request, **kwargs)
    assert form_field is not None