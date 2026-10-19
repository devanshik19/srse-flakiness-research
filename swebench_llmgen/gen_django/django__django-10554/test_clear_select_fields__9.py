import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet

def test_clear_select_fields():
    # Create a QuerySet based on the User model
    queryset = User.objects.all()

    # Verify that initial select fields are set
    assert isinstance(queryset.query.select, tuple)
    assert queryset.query.select == ()

    # Set select fields
    queryset = queryset.values('username', 'email')
    
    # Verify that select fields are correctly set
    assert isinstance(queryset.query.values_select, tuple)
    assert queryset.query.values_select == ('username', 'email')

    # Call the clear_select_fields method
    queryset.query.clear_select_fields()

    # Verify that fields are cleared
    assert queryset.query.select == ()
    assert queryset.query.values_select == ()