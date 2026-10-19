import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query


@pytest.mark.django_db
def test_clear_select_fields():
    # Create a Query object
    query = Query(User)

    # Initial state: set select fields
    query.set_select(('username', 'email'))

    # Check select fields are set
    assert query.select == ('username', 'email')
    assert query.values_select == ()

    # Call the clear_select_fields method
    query.clear_select_fields()

    # Check that the select fields are cleared
    assert query.select == ()
    assert query.values_select == ()

    # Test behavior after clearing (no errors should occur when querying after clearing)
    # This is just to confirm that the query object maintains integrity after clearing
    assert query.has_select_fields() is False