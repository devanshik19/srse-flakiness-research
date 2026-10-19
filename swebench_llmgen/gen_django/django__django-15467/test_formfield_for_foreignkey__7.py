import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.admin import widgets

class TestBaseModelAdmin:

    class BaseModelAdminStub:
        admin_site = site
        autocomplete_fields = ['related_field']
        raw_id_fields = ['user']
        radio_fields = {
            'select_field': ('input_type',)
        }

        def get_autocomplete_fields(self, request):
            return self.autocomplete_fields

        def get_field_queryset(self, db, db_field, request):
            if db_field.name == 'user':
                return User.objects.all()
            return None

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            db = kwargs.get("using")

            if "widget" not in kwargs:
                if db_field.name in self.get_autocomplete_fields(request):
                    kwargs["widget"] = AutocompleteSelect(
                        db_field, self.admin_site, using=db
                    )
                elif db_field.name in self.raw_id_fields:
                    kwargs["widget"] = widgets.ForeignKeyRawIdWidget(
                        db_field.remote_field, self.admin_site, using=db
                    )
                elif db_field.name in self.radio_fields:
                    kwargs["widget"] = widgets.AdminRadioSelect(
                        attrs={
                            "class": "admin-radio",
                        }
                    )
                    kwargs["empty_label"] = _("None") if db_field.blank else None

            if "queryset" not in kwargs:
                queryset = self.get_field_queryset(db, db_field, request)
                if queryset is not None:
                    kwargs["queryset"] = queryset

            return db_field.formfield(**kwargs)

    @pytest.fixture
    def admin_stub(self):
        return self.BaseModelAdminStub()

    def test_formfield_for_foreignkey_autocomplete_widget(self, admin_stub):
        field = models.ForeignKey(User, on_delete=models.CASCADE, name='related_field')
        request = None
        
        formfield = admin_stub.formfield_for_foreignkey(field, request)
        assert isinstance(formfield.widget, AutocompleteSelect)

    def test_formfield_for_foreignkey_raw_id_widget(self, admin_stub):
        field = models.ForeignKey(User, on_delete=models.CASCADE, name='user')
        request = None
        
        formfield = admin_stub.formfield_for_foreignkey(field, request)
        assert isinstance(formfield.widget, widgets.ForeignKeyRawIdWidget)

    def test_formfield_for_foreignkey_radio_widget(self, admin_stub):
        field = models.ForeignKey(User, on_delete=models.CASCADE, name='select_field')
        request = None
        
        formfield = admin_stub.formfield_for_foreignkey(field, request)
        assert isinstance(formfield.widget, widgets.AdminRadioSelect)
        assert formfield.empty_label is None  # Assuming field is not blank