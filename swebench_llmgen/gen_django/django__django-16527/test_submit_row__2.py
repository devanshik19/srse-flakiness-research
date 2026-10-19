import json
from django import template
from django.template.context import Context
from django.contrib.auth.models import User
from django.contrib.admin.templatetags.admin_modify import submit_row

def test_submit_row():
    # Test case setup
    context = {
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
        "has_delete_permission": True,
        "show_delete": True,
    }
    
    expected_keys = [
        "can_change",
        "show_delete_link",
        "show_save_as_new",
        "show_save_and_add_another",
        "show_save_and_continue",
        "show_save",
        "show_close"
    ]
    
    # Invoke the function
    ctx = submit_row(context)
    
    # Assert expected keys are in the context returned
    assert all(key in ctx for key in expected_keys)
    
    # Assert values for the context
    assert ctx["can_change"] is False
    assert ctx["show_delete_link"] is False
    assert ctx["show_save_as_new"] is False
    assert ctx["show_save_and_add_another"] is True
    assert ctx["show_save_and_continue"] is True
    assert ctx["show_save"] is True
    assert ctx["show_close"] is False

    # Testing with scenario where change = True
    context["change"] = True
    context["has_change_permission"] = True
    context["has_delete_permission"] = False
    
    ctx = submit_row(context)
    
    assert ctx["can_change"] is True
    assert ctx["show_delete_link"] is False
    assert ctx["show_save_as_new"] is False
    assert ctx["show_save_and_add_another"] is True
    assert ctx["show_save_and_continue"] is True
    assert ctx["show_save"] is True
    assert ctx["show_close"] is False

    # Testing with save_as condition
    context["save_as"] = True
    ctx = submit_row(context)
    
    assert ctx["show_save_as_new"] is True
    
    # Testing with popup condition
    context["is_popup"] = True
    ctx = submit_row(context)
    
    assert ctx["show_save_and_add_another"] is False
    assert ctx["show_save_and_continue"] is False
    assert ctx["show_save"] is False
    assert ctx["show_delete_link"] is False