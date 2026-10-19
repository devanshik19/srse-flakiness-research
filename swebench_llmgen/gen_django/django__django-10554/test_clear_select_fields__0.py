import pytest
from django.db.models import QuerySet
from django.contrib.auth.models import User

def test_clear_select_fields():
    # Setup: Create a QuerySet with some selected fields
    qs = User.objects.values('id', 'username', 'email')
    
    # Assert that the QuerySet has select fields
    assert len(qs.query.select) > 0

    # Call the clear_select_fields method
    qs.query.clear_select_fields()
    
    # Assert that the select fields are cleared
    assert len(qs.query.select) == 0
    assert len(qs.query.values_select) == 0

    # To further validate, we can check the QuerySet's behavior
    assert list(qs) == list(User.objects.all())