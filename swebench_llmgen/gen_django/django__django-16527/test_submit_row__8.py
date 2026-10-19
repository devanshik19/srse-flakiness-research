import json
from django import template
from django.template.context import Context
from django.contrib.auth.models import User
from django.contrib.admin.templatetags.admin_modify import submit_row
import pytest

@pytest.mark.parametrize("context, expected_keys", [
    ({
        "add": False,
        "change": True,
        "is_popup": False,
        "save_as": False,
        "has_add_permission": True,
        "has_change_permission": True,
        "has_view_permission": True,
        "has_editable_inline_admin_formsets": False,
        "has_delete_permission": True,
        "show_save": True,
        "show_save_and_add_another": True,
        "show_save_and_continue": True,
        "show_delete": True,
    }, ["can_change", "show_delete_link", "show_save_as_new", "show_save_and_add_another", "show_save_and_continue", "show_save", "show_close"]),
    ({
        "add": True,
        "change": False,
        "is_popup": True,
        "save_as": True,
        "has_add_permission": False,
        "has_change_permission": False,
        "has_view_permission": True,
        "has_editable_inline_admin_formsets": True,
        "has_delete_permission": True,
    }, ["can_change", "show_delete_link", "show_save_as_new", "show_save_and_add_another", "show_save_and_continue", "show_save", "show_close"]),
])
def test_submit_row(context, expected_keys):
    ctx = submit_row(context)
    assert isinstance(ctx, Context)
    
    for key in expected_keys:
        assert key in ctx