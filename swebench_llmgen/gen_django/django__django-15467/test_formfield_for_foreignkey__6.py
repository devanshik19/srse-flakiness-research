import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.admin import widgets
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe


class SampleAdmin:
    autocomplete_fields = ['related_user']
    raw_id_fields = []
    radio_fields = {}
    admin_site = site


class RelatedModel(models.Model):
    related_user = models.ForeignKey(User, on_delete=models.CASCADE)


class SampleForm(ModelForm):
    class Meta:
        model = RelatedModel
        fields = '__all__'


@pytest.mark.parametrize("widget_type, expected_widget", [
    (None, AutocompleteSelect),
    ([], widgets.ForeignKeyRawIdWidget),
])
def test_formfield_for_foreignkey(widget_type, expected_widget):
    admin = SampleAdmin()
    db_field = RelatedModel._meta.get_field('related_user')

    # Prepare request simulation
    class Request:
        pass

    request = Request()

    kwargs = {"widget": widget_type}
    field = admin.formfield_for_foreignkey(db_field, request, **kwargs)

    assert isinstance(field.widget, expected_widget) if widget_type is None else not isinstance(field.widget, expected_widget)
    assert field.name == 'related_user'
    assert 'queryset' in kwargs or field.queryset is not None