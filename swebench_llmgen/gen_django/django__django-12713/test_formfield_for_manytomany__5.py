import pytest
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

class TestModel(models.Model):
    users = models.ManyToManyField(User)

class TestModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['users']
    raw_id_fields = ['users']
    filter_vertical = ['users']

    def get_field_queryset(self, db, db_field, request):
        return User.objects.all()

    def get_autocomplete_fields(self, request):
        return self.autocomplete_fields

@pytest.mark.parametrize(
    "db_field_name, expected_widget_type",
    [
        ("users", forms.SelectMultiple),  # testing with autocomplete
        ("users", admin.widgets.ManyToManyRawIdWidget),  # testing with raw_id_fields
        ("users", admin.widgets.FilteredSelectMultiple)  # testing with filter_horizontal
    ]
)
def test_formfield_for_manytomany(db_field_name, expected_widget_type):
    model_admin = TestModelAdmin(TestModel, admin.site)

    db_field = TestModel._meta.get_field(db_field_name)
    form_field = model_admin.formfield_for_manytomany(db_field, None)

    assert isinstance(form_field.widget, expected_widget_type)
    assert form_field.queryset.count() == User.objects.count()

    # Check that help_text is updated if the widget is a SelectMultiple
    if isinstance(form_field.widget, forms.SelectMultiple):
        assert "Hold down “Control”, or “Command” on a Mac, to select more than one." in form_field.help_text

def test_formfield_for_manytomany_no_intermediary():
    model_admin = TestModelAdmin(TestModel, admin.site)
    class AnotherTestModel(models.Model):
        users = models.ManyToManyField(User, through='IntermediateModel')

    db_field = AnotherTestModel._meta.get_field('users')
    form_field = model_admin.formfield_for_manytomany(db_field, None)
    assert form_field is None