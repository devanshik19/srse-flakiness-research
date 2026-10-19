import pytest
from django.contrib.auth.models import User
from django.db.models import Query

def test_clear_select_fields():
    # Setup a Query object with select fields
    user_queryset = User.objects.all()
    query = user_queryset.query
    
    # Ensure there are select fields before clearing
    assert query.select != ()

    # Call the method to clear select fields
    query.clear_select_fields()

    # Verify that the select fields are cleared
    assert query.select == ()
    assert query.values_select == ()