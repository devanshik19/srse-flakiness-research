import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_clear_select_fields():
    # Create a Query instance
    user_queryset = User.objects.all()
    query = user_queryset.query

    # Set some fields to select
    query.set_select(('username', 'email'))

    # Ensure fields are set
    assert query.select == ('username', 'email')
    assert query.values_select == ()

    # Call clear_select_fields
    query.clear_select_fields()

    # Assert that select fields are cleared
    assert query.select == ()
    assert query.values_select == ()