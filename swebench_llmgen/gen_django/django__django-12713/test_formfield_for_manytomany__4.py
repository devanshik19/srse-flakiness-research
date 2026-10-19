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

    def get_autocomplete_fields(self, request):
        return self.autocomplete_fields

    def get_field_queryset(self, using, db_field, request):
        return User.objects.all()

class TestFormFieldForManyToMany:
    @pytest.fixture
    def admin_instance(self):
        return TestModelAdmin(TestModel, admin.site)

    @pytest.fixture
    def request(self):
        class Request:
            pass
        return Request()

    def test_formfield_for_manytomany_with_autocomplete(self, admin_instance, request):
        db_field = TestModel._meta.get_field('users')
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        
        assert isinstance(form_field.widget, admin.widgets.AutocompleteSelectMultiple)

    def test_formfield_for_manytomany_without_intermediary(self, admin_instance, request):
        db_field = TestModel._meta.get_field('users')
        db_field.remote_field.through._meta.auto_created = False
        
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        
        assert form_field is None

    def test_formfield_for_manytomany_with_raw_id_field(self, admin_instance, request):
        admin_instance.raw_id_fields = ['users']
        db_field = TestModel._meta.get_field('users')
        
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        
        assert isinstance(form_field.widget, admin.widgets.ManyToManyRawIdWidget)

    def test_formfield_for_manytomany_with_filter_vertical(self, admin_instance, request):
        admin_instance.filter_vertical = ['users']
        db_field = TestModel._meta.get_field('users')
        
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        
        assert isinstance(form_field.widget, admin.widgets.FilteredSelectMultiple)

    def test_formfield_for_manytomany_adds_help_text(self, admin_instance, request):
        db_field = TestModel._meta.get_field('users')
        form_field = admin_instance.formfield_for_manytomany(db_field, request)
        
        assert 'Hold down “Control”, or “Command” on a Mac, to select more than one.' in form_field.help_text