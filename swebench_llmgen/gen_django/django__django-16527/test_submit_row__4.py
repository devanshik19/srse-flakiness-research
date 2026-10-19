import pytest
from django import template
from django.template.context import Context
from django.contrib.auth.models import User
from django.contrib.admin.templatetags.admin_modify import submit_row

@pytest.mark.parametrize("context", [
    {
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
    },
    {
        "add": False,
        "change": True,
        "is_popup": False,
        "save_as": True,
        "show_save": True,
        "show_save_and_add_another": False,
        "show_save_and_continue": True,
        "has_add_permission": False,
        "has_change_permission": True,
        "has_view_permission": True,
        "has_editable_inline_admin_formsets": False,
        "has_delete_permission": True
    },
    {
        "add": True,
        "change": False,
        "is_popup": True,
        "save_as": False,
        "show_save": True,
        "show_save_and_add_another": True,
        "show_save_and_continue": True,
        "has_add_permission": True,
        "has_change_permission": True,
        "has_view_permission": True,
        "has_editable_inline_admin_formsets": False,
        "has_delete_permission": True
    },
    {
        "add": False,
        "change": True,
        "is_popup": False,
        "save_as": False,
        "show_save": False,
        "show_save_and_add_another": True,
        "show_save_and_continue": True,
        "has_add_permission": True,
        "has_change_permission": True,
        "has_view_permission": False,
        "has_editable_inline_admin_formsets": True,
        "has_delete_permission": False
    },
])
def test_submit_row(context):
    expected_keys = [
        "can_change",
        "show_delete_link",
        "show_save_as_new",
        "show_save_and_add_another",
        "show_save_and_continue",
        "show_save",
        "show_close",
    ]

    result = submit_row(context)

    assert isinstance(result, Context)
    for key in expected_keys:
        assert key in result
    assert result['can_change'] == (context['has_change_permission'] or context['has_editable_inline_admin_formsets'])
    assert result['show_delete_link'] == (
        not context['is_popup']
        and context['has_delete_permission']
        and context['change']
        and context.get("show_delete", True)
    )
    assert result['show_save_and_add_another'] == (
        context['has_add_permission']
        and not context['is_popup']
        and (not context['save_as'] or context['add'])
        and (
            (context['has_change_permission'] and context['change']) 
            or (context['has_add_permission'] and context['add']) 
            or context['has_editable_inline_admin_formsets']
        )
        and context['show_save_and_add_another']
    )
    assert result['show_save_and_continue'] == (
        not context['is_popup']
        and (
            (context['has_change_permission'] and context['change']) 
            or (context['has_add_permission'] and context['add']) 
            or context['has_editable_inline_admin_formsets']
        )
        and context['has_view_permission']
        and context['show_save_and_continue']
    )
    assert result['show_save'] == (context['show_save'] and (
        (context['has_change_permission'] and context['change']) 
        or (context['has_add_permission'] and context['add']) 
        or context['has_editable_inline_admin_formsets']
    ))
    assert result['show_close'] == not (context['show_save'] and (
        (context['has_change_permission'] and context['change']) 
        or (context['has_add_permission'] and context['add']) 
        or context['has_editable_inline_admin_formsets']
    ))