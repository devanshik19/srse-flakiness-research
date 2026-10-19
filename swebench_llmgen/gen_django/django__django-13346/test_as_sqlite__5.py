import json
import pytest
from django.db import connections
from django.db.models import F
from django.contrib.auth.models import User
from ..fields.json import HasKeyLookup

def test_as_sqlite():
    # Arrange
    compiler = connections['default'].schema_editor()  # Using schema_editor as a stand-in for the SQL compiler
    connection = connections['default']
    key_lookup = HasKeyLookup()
    
    # Act
    sql = key_lookup.as_sqlite(compiler, connection)

    # Assert
    expected_sql = 'JSON_TYPE(%s, %s) IS NOT NULL'
    assert expected_sql in sql
    
    # Test with a valid instance
    user = User.objects.create_user(username='testuser', password='testpass')
    key = 'name'
    assert key in user.__dict__.keys()  # Make sure the user instance has the 'name' field