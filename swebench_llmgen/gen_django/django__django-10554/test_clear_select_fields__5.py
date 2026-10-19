import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_clear_select_fields():
    # Arrange
    query = Query(User)
    # Simulate having some selected fields
    query.select = ('username', 'email')
    query.values_select = ('username', 'email')

    # Act
    query.clear_select_fields()

    # Assert
    assert query.select == ()
    assert query.values_select == ()