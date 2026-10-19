import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.contrib.admin import widgets
from django.utils.translation import gettext as _
from django.contrib.admin.options import BaseModelAdmin


class TestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TestModelAdmin(BaseModelAdmin):
    autocomplete_fields = ['user']
    raw_id_fields = []
    radio_fields = {}


@pytest.mark.django_db
def test_formfield_for_foreignkey_with_autocomplete_fields():
    admin = TestModelAdmin(TestModel, site)
    field = TestModel._meta.get_field('user')
    request = None  # Simulating without an actual HttpRequest

    form_field = admin.formfield_for_foreignkey(field, request)

    assert isinstance(form_field.widget, widgets.AutocompleteSelect)
    assert form_field.queryset.model is User.objects


@pytest.mark.django_db
def test_formfield_for_foreignkey_with_raw_id_fields():
    admin = TestModelAdmin(TestModel, site)
    admin.raw_id_fields = ['user']
    field = TestModel._meta.get_field('user')
    request = None  # Simulating without an actual HttpRequest

    form_field = admin.formfield_for_foreignkey(field, request)

    assert isinstance(form_field.widget, widgets.ForeignKeyRawIdWidget)


@pytest.mark.django_db
def test_formfield_for_foreignkey_with_radio_fields():
    admin = TestModelAdmin(TestModel, site)
    admin.radio_fields = {'user': 'radio'}
    field = TestModel._meta.get_field('user')
    request = None  # Simulating without an actual HttpRequest

    form_field = admin.formfield_for_foreignkey(field, request)

    assert isinstance(form_field.widget, widgets.AdminRadioSelect)
    assert form_field.empty_label == _("None")


@pytest.mark.django_db
def test_formfield_for_foreignkey_with_queryset():
    admin = TestModelAdmin(TestModel, site)
    field = TestModel._meta.get_field('user')
    request = None  # Simulating without an actual HttpRequest
    
    # Assuming the get_field_queryset method only affects db_field queryset
    def custom_queryset(db, db_field, request):
        return User.objects.filter(is_active=True)

    admin.get_field_queryset = custom_queryset
    form_field = admin.formfield_for_foreignkey(field, request)

    assert form_field.queryset.count() == User.objects.filter(is_active=True).count()