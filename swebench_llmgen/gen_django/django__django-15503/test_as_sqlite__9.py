import json
import pytest
from django.db import connections
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.fields.json import HasKeyLookup

def test_as_sqlite():
    # Arrange
    user = User.objects.create(username='testuser', password='password', email='test@example.com')
    lookup = HasKeyLookup()
    compiler = connections['default'].cursor()

    # Act
    sql = lookup.as_sqlite(compiler, connections['default'])

    # Assert
    assert "JSON_TYPE(%s, %%s) IS NOT NULL" in sql
    assert isinstance(sql, str)

    # Test if the inclusion of the actual query works
    q = Q(**{lookup.logical_operator: 'some_key'})
    query = user.objects.filter(q)

    assert len(query) == 1
    assert query[0].username == 'testuser'