import json
import pytest
from django.contrib.auth.models import User
from django.db.models import Func
from django.db.models.fields.json import HasKeyLookup

class JSONType(Func):
    function = 'JSON_TYPE'

@pytest.mark.parametrize('key, expected_sql', [
    ('test_key', 'JSON_TYPE(%s, %s) IS NOT NULL'),
])
def test_as_sqlite(key, expected_sql):
    # Arrange
    compiler = User.objects._query.__class__.__dict__['compiler'](User.objects.db)
    connection = User.objects.db

    # Instantiate HasKeyLookup
    lookup = HasKeyLookup()
    
    # Act
    sql = lookup.as_sqlite(compiler, connection)

    # Assert
    assert sql[0] == expected_sql, f"Expected SQL pattern: {expected_sql}, got: {sql[0]}"