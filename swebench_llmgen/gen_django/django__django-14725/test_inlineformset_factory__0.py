import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms.models import ModelForm

# Create a simple model form for testing
class TestModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

def test_inlineformset_factory():
    # Define a simple parent model and child model
    parent_user = User.objects.create_user(username='parent', email='parent@example.com', password='password')

    # Create an Inline FormSet using the inlineformset_factory
    InlineFormSet = inlineformset_factory(User, User, form=TestModelForm, extra=2, can_delete=True)
    
    # Create the formset instance
    formset = InlineFormSet(instance=parent_user)

    # Assert initial empty forms
    assert len(formset.forms) == 2
    for form in formset.forms:
        assert 'username' in form.fields
        assert 'email' in form.fields

    # Populate the formset with data
    formset_data = {'username': ['child1', 'child2'], 'email': ['child1@example.com', 'child2@example.com'], 'DELETE': ['False', 'False']}
    formset = InlineFormSet(data=formset_data, instance=parent_user)

    # Validate formset
    assert formset.is_valid()
    assert formset.total_form_count() == 2

    # Save the formset and check instances
    formset.save()
    
    # Check if the instances were created correctly
    assert User.objects.filter(username='child1').exists()
    assert User.objects.filter(username='child2').exists()

    # Now test the can_delete functionality
    formset = InlineFormSet(data={'username': ['child1'], 'email': ['child1@example.com'], 'DELETE': ['True']}, instance=parent_user)
    assert formset.is_valid()
    formset.save()
    
    # Assert that 'child1' has been deleted
    assert not User.objects.filter(username='child1').exists()
    assert User.objects.filter(username='child2').exists()