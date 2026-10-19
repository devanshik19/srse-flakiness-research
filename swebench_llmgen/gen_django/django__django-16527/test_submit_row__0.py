import pytest
from django import template
from django.template.context import Context
from django.contrib.auth.models import User
from django.contrib.admin.templatetags.admin_modify import submit_row

@pytest.mark.parametrize("context,expected", [
    ({
        "add": True,
        "change": False,
        "is_popup": False,
        "save_as": False,
        "show_save": True,
        "show_save_and_add_another": True,
        "show_save_and_continue": True,
        "has_add_permission": True,
        "has_change_permission": False,
        "has_view_permission": True,
        "has_editable_inline_admin_formsets": False,
        "has_delete_permission": True
    }, {
        "can_change": False,
        "show_delete_link": True,
        "show_save_as_new": False,
        "show_save_and_add_another": True,
        "show_save_and_continue": False,
        "show_save": True,
        "show_close": False,
    }),
    ({
        "add": False,
        "change": True,
        "is_popup": True,
        "save_as": True,
        "show_save": False,
        "show_save_and_add_another": False,
        "show_save_and_continue": False,
        "has_add_permission": False,
        "has_change_permission": True,
        "has_view_permission": False,
        "has_editable_inline_admin_formsets": False,
        "has_delete_permission": False
    }, {
        "can_change": True,
        "show_delete_link": False,
        "show_save_as_new": False,
        "show_save_and_add_another": False,
        "show_save_and_continue": False,
        "show_save": False,
        "show_close": True,
    }),
    ({
        "add": True,
        "change": True,
        "is_popup": False,
        "save_as": True,
        "show_save": True,
        "show_save_and_add_another": True,
        "show_save_and_continue": True,
        "has_add_permission": True,
        "has_change_permission": True,
        "has_view_permission": True,
        "has_editable_inline_admin_formsets": True,
        "has_delete_permission": True
    }, {
        "can_change": True,
        "show_delete_link": True,
        "show_save_as_new": True,
        "show_save_and_add_another": True,
        "show_save_and_continue": True,
        "show_save": True,
        "show_close": False,
    }),
])
def test_submit_row(context, expected):
    result = submit_row(context)
    for key, value in expected.items():
        assert result[key] == value