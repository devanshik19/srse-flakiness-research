import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.forms.models import BaseInlineFormSet, inlineformset_factory

# Test function for inlineformset_factory
def test_inlineformset_factory():
    class AddressForm(forms.ModelForm):
        class Meta:
            model = User  # Using User model for this example
            fields = ['username', 'email']

    class AddressInlineFormSet(BaseInlineFormSet):
        pass

    # Create an inline formset factory for User model
    UserAddressFormSet = inlineformset_factory(
        parent_model=User,
        model=User,
        form=AddressForm,
        formset=AddressInlineFormSet,
        fk_name='username',  # Using 'username' as a placeholder for ForeignKey
        extra=2,
        can_delete=True,
    )

    # Create a parent model instance
    parent_user = User.objects.create(username='parent_user', email='parent@example.com')

    # Test create formset with extra forms
    formset = UserAddressFormSet(instance=parent_user)
    assert len(formset) == 2  # Check that we have the correct number of forms

    # Test form validation
    data = {
        'username': ['child_user1', 'child_user2'],
        'email': ['child1@example.com', 'child2@example.com'],
        'DELETE': [False, False],
    }
    formset = UserAddressFormSet(data=data, instance=parent_user)
    assert formset.is_valid()  # Should be valid with correct data

    # Test formset with invalid data
    data['email'][0] = ''  # Making first email invalid
    formset = UserAddressFormSet(data=data, instance=parent_user)
    assert not formset.is_valid()  # Should be invalid due to empty email
    assert 'email' in formset.errors[0]  # Check for errors on the first form

    # Test max_num enforcement
    UserAddressFormSet = inlineformset_factory(
        parent_model=User,
        model=User,
        form=AddressForm,
        formset=AddressInlineFormSet,
        fk_name='username',
        max_num=1  # Set max_num to 1
    )

    formset = UserAddressFormSet(instance=parent_user)
    assert len(formset) == 1  # Should only allow 1 form

    # Check if foreign key field is set correctly
    assert hasattr(UserAddressFormSet, 'fk')