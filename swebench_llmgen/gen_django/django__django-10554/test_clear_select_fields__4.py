import pytest
from django.db.models import Query
from django.contrib.auth.models import User

def test_clear_select_fields():
    # Create an instance of Query using a User model (assuming it's required)
    query = Query(User)

    # Set some fields to select before clearing
    query.select = ('username', 'email')
    query.values_select = ('first_name', 'last_name')

    # Ensure that the select fields are populated before calling the method
    assert query.select == ('username', 'email')
    assert query.values_select == ('first_name', 'last_name')

    # Call the clear_select_fields method
    query.clear_select_fields()

    # Assert that the select fields are cleared
    assert query.select == ()
    assert query.values_select == ()