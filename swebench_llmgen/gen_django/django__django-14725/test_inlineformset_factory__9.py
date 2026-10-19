import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, BaseInlineFormSet


class AddressForm(forms.ModelForm):
    class Meta:
        model = User  # Using User as a stand-in for another model
        fields = ['username']  # Simplifying for test purposes


@pytest.mark.django_db
def test_inlineformset_factory():
    # Create a parent model instance
    parent_user = User.objects.create(username='parent_user')

    # Create the inline formset
    InlineFormSet = inlineformset_factory(User, User, form=AddressForm, extra=2)

    formset = InlineFormSet(instance=parent_user)

    assert isinstance(formset, BaseInlineFormSet)
    assert formset.extra == 2
    assert formset.can_delete is True
    assert len(formset.forms) == 2

    # Check that the FK is set correctly
    assert formset.fk.name == 'user'  # Replace 'user' with the correct field name if needed

    # Test adding data to the formset
    formset_data = {
        'form-0-username': 'child_user_1',
        'form-1-username': 'child_user_2',
        'form-2-username': '',  # This one should be empty
        'form-0-DELETE': 'False',
        'form-1-DELETE': 'False',
        'form-TOTAL_FORMS': '3',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
    }
    formset = InlineFormSet(data=formset_data, instance=parent_user)
    
    assert formset.is_valid()
    formset.save()

    # Check that two new users were created
    assert User.objects.filter(username='child_user_1').exists()
    assert User.objects.filter(username='child_user_2').exists()
    assert User.objects.filter(username='parent_user').exists()

    # Test for the case when fk is unique
    InlineFormSetUnique = inlineformset_factory(User, User, form=AddressForm, max_num=1)

    formset_unique = InlineFormSetUnique(instance=parent_user)

    assert formset_unique.max_num == 1

    # Test creating with unique foreign key
    formset_data_unique = {
        'form-0-username': 'child_user_unique',
        'form-0-DELETE': 'False',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '1',
    }
    formset_unique = InlineFormSetUnique(data=formset_data_unique, instance=parent_user)
    
    assert formset_unique.is_valid()
    formset_unique.save()

    # Check that the unique user has been created
    assert User.objects.filter(username='child_user_unique').exists()