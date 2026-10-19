import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

class TestManyToManyFieldAdmin(admin.ModelAdmin):
    def get_autocomplete_fields(self, request):
        return ['related_users']

class RelatedModel(models.Model):
    users = models.ManyToManyField(User, related_name='related_models')

class TestBaseModelAdmin:
    @pytest.fixture
    def admin_instance(self):
        return TestManyToManyFieldAdmin(RelatedModel, admin.site)

    @pytest.fixture
    def db_field(self):
        return RelatedModel._meta.get_field('users')

    @pytest.fixture
    def request(self, rf):
        return rf.get('/admin/')

    def test_formfield_for_manytomany_autocomplete(self, admin_instance, db_field, request):
        admin_instance.autocomplete_fields = ['related_users']
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        assert isinstance(form_field.widget, admin.widgets.AutocompleteSelectMultiple)

    def test_formfield_for_manytomany_raw_id_fields(self, admin_instance, db_field, request):
        admin_instance.raw_id_fields = ['users']
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        assert isinstance(form_field.widget, admin.widgets.ManyToManyRawIdWidget)

    def test_formfield_for_manytomany_filter_vertical(self, admin_instance, db_field, request):
        admin_instance.filter_vertical = ['users']
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        assert isinstance(form_field.widget, admin.widgets.FilteredSelectMultiple)

    def test_formfield_for_manytomany_no_widget(self, admin_instance, db_field, request):
        db_field.remote_field.through._meta.auto_created = False
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        assert form_field is None

    def test_formfield_for_manytomany_help_text(self, admin_instance, db_field, request):
        db_field.remote_field.through._meta.auto_created = True
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        form_field.help_text = 'Test help text'
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        assert 'Hold down “Control”, or “Command” on a Mac, to select more than one.' in form_field.help_text