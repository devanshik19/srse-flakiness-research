import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

@pytest.mark.parametrize("fk_name, unique, expected_max_num", [
    (None, False, 3),
    (None, True, 1),
])
def test_inlineformset_factory(fk_name, unique, expected_max_num):
    class ChildModel(forms.ModelForm):
        class Meta:
            model = User  # Use User as a stand-in for the child model
            fields = ['username', 'first_name', 'last_name']

    # Mock the _get_foreign_key function to control its output
    def mock_get_foreign_key(parent_model, model, fk_name):
        class ForeignKey:
            unique = unique

        return ForeignKey()

    # Replace _get_foreign_key with the mock
    global _get_foreign_key
    original_get_foreign_key = _get_foreign_key
    _get_foreign_key = mock_get_foreign_key

    FormSet = inlineformset_factory(User, User, form=ChildModel, fk_name=fk_name)
    
    assert FormSet.extra == 3
    assert FormSet.max_num == expected_max_num

    # Restore the original function
    _get_foreign_key = original_get_foreign_key