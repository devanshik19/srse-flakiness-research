import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet

def test_clear_select_fields():
    # Create a QuerySet for User model
    qs = User.objects.all()

    # Apply some selection fields using values()
    qs = qs.values('username', 'email')

    # Check that select fields are set correctly
    assert qs.query.select == (('username',), ('email',))

    # Calling the clear_select_fields method
    qs._query.clear_select_fields()

    # Assert that select fields are cleared
    assert qs.query.select == ()
    assert qs.query.values_select == ()