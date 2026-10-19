import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

# Define a simple ManyToMany relationship for testing
class Group(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='groups')


class GroupAdmin(admin.ModelAdmin):
    autocomplete_fields = ['users']
    raw_id_fields = []
    filter_horizontal = []
    filter_vertical = []

    def get_field_queryset(self, db, db_field, request):
        return User.objects.all()

    def get_autocomplete_fields(self, request):
        return self.autocomplete_fields


@pytest.fixture
def admin_site():
    return admin.site


@pytest.fixture
def group_admin(admin_site):
    return GroupAdmin(Group, admin_site)


@pytest.mark.parametrize("m2m_field, expected_widget", [
    ('users', 'AutocompleteSelectMultiple'),
    ('users', 'ManyToManyRawIdWidget'),
    ('users', 'FilteredSelectMultiple'),
])
def test_formfield_for_manytomany(group_admin, m2m_field, expected_widget, django_user_model):
    # Prepare a mock request
    class MockRequest:
        user = django_user_model()

    db_field = Group._meta.get_field(m2m_field)
    form_field = group_admin.formfield_for_manytomany(db_field, MockRequest())

    assert form_field is not None
    assert expected_widget in str(type(form_field.widget))

    # Check if queryset is correctly assigned
    assert form_field.queryset.count() == User.objects.count()

    # Check the help text
    help_text = form_field.help_text
    assert 'Hold down “Control”, or “Command” on a Mac, to select more than one.' in help_text