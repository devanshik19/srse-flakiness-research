import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext as _
from django.contrib.admin.widgets import AutocompleteSelectMultiple, FilteredSelectMultiple
from django.contrib.admin import widgets

class Group(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='groups')

class GroupAdmin:
    autocomplete_fields = []
    raw_id_fields = []
    filter_vertical = []
    filter_horizontal = ['users']

    def get_autocomplete_fields(self, request):
        return self.autocomplete_fields

    def get_field_queryset(self, db, db_field, request):
        return User.objects.all()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not db_field.remote_field.through._meta.auto_created:
            return None
        db = kwargs.get('using')

        autocomplete_fields = self.get_autocomplete_fields(request)
        if db_field.name in autocomplete_fields:
            kwargs['widget'] = AutocompleteSelectMultiple(db_field.remote_field, site, using=db)
        elif db_field.name in self.raw_id_fields:
            kwargs['widget'] = widgets.ManyToManyRawIdWidget(db_field.remote_field, site, using=db)
        elif db_field.name in [*self.filter_vertical, *self.filter_horizontal]:
            kwargs['widget'] = FilteredSelectMultiple(
                db_field.verbose_name,
                db_field.name in self.filter_vertical
            )

        if 'queryset' not in kwargs:
            queryset = self.get_field_queryset(db, db_field, request)
            if queryset is not None:
                kwargs['queryset'] = queryset

        form_field = db_field.formfield(**kwargs)
        if (isinstance(form_field.widget, widgets.SelectMultiple) and
                not isinstance(form_field.widget, (widgets.CheckboxSelectMultiple, AutocompleteSelectMultiple))):
            msg = _('Hold down “Control”, or “Command” on a Mac, to select more than one.')
            help_text = form_field.help_text
            form_field.help_text = f"{help_text} {msg}" if help_text else msg
        return form_field

@pytest.mark.django_db
def test_formfield_for_manytomany():
    admin = GroupAdmin()
    
    group_field = Group._meta.get_field('users')
    request = None  # Mock request; specifics are not necessary for this test

    # Test with filter_horizontal
    form_field = admin.formfield_for_manytomany(group_field, request)
    assert isinstance(form_field.widget, FilteredSelectMultiple)

    # Test with raw_id_fields being empty
    admin.raw_id_fields = []
    admin.filter_horizontal = []
    form_field = admin.formfield_for_manytomany(group_field, request)
    assert isinstance(form_field.widget, FilteredSelectMultiple)

    # Manually set it to use raw_id_fields
    admin.raw_id_fields = ['users']
    form_field = admin.formfield_for_manytomany(group_field, request)
    assert isinstance(form_field.widget, widgets.ManyToManyRawIdWidget)

    # Test when there is an intermediary model that is not auto created
    group_field.remote_field.through = models.Model  # Simulate a user-defined intermediary
    form_field = admin.formfield_for_manytomany(group_field, request)
    assert form_field is None

    # Reset for the last test case
    admin.raw_id_fields = []
    group_field.remote_field.through._meta.auto_created = True
    form_field = admin.formfield_for_manytomany(group_field, request)
    assert form_field is not None