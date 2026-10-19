import json
from django import template
from django.template.context import Context
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.contrib.admin.views.main import ChangeList
from .admin_modify import submit_row

def test_submit_row_with_all_permissions():
    context = {
        'add': False,
        'change': True,
        'is_popup': False,
        'save_as': False,
        'show_save': True,
        'show_save_and_add_another': True,
        'show_save_and_continue': True,
        'has_add_permission': True,
        'has_change_permission': True,
        'has_view_permission': True,
        'has_editable_inline_admin_formsets': True,
        'has_delete_permission': True,
        'show_delete': True,
    }
    
    result = submit_row(context)
    
    assert result['can_change'] is True
    assert result['show_delete_link'] is True
    assert result['show_save_as_new'] is True
    assert result['show_save_and_add_another'] is True
    assert result['show_save_and_continue'] is True
    assert result['show_save'] is True
    assert result['show_close'] is False


def test_submit_row_without_add_permission():
    context = {
        'add': False,
        'change': True,
        'is_popup': False,
        'save_as': False,
        'show_save': True,
        'show_save_and_add_another': True,
        'show_save_and_continue': True,
        'has_add_permission': False,
        'has_change_permission': True,
        'has_view_permission': True,
        'has_editable_inline_admin_formsets': False,
        'has_delete_permission': True,
        'show_delete': True,
    }

    result = submit_row(context)

    assert result['can_change'] is True
    assert result['show_delete_link'] is True
    assert result['show_save_as_new'] is False
    assert result['show_save_and_add_another'] is False
    assert result['show_save_and_continue'] is True
    assert result['show_save'] is True
    assert result['show_close'] is False


def test_submit_row_empty_context():
    context = {
        'add': False,
        'change': False,
        'is_popup': False,
        'save_as': False,
        'has_add_permission': False,
        'has_change_permission': False,
        'has_view_permission': False,
        'has_editable_inline_admin_formsets': False,
        'has_delete_permission': False,
        'show_delete': True,
    }
    
    result = submit_row(context)
    
    assert result['can_change'] is False
    assert result['show_delete_link'] is False
    assert result['show_save_as_new'] is False
    assert result['show_save_and_add_another'] is False
    assert result['show_save_and_continue'] is False
    assert result['show_save'] is False
    assert result['show_close'] is True