import json
import pytest
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.expressions import RawSQL
from django.db.models.fields.json import HasKeyLookup

@pytest.mark.parametrize("path", [
    "$.key1",
    "$.key2.subkey",
    "$.key3[*].subkey",
])
def test_as_oracle(path):
    lookup = HasKeyLookup()
    user = User.objects.create(username='testuser', password='password')

    # Simulate a JSONField for testing
    user.profile_data = json.dumps({
        "key1": "value1",
        "key2": {
            "subkey": "value2"
        },
        "key3": [
            {"subkey": "value3"},
            {"subkey": "value4"}
        ]
    })
    user.save()

    # Perform the lookup
    sql, params = lookup.as_oracle(None, None)

    assert "JSON_EXISTS" in sql
    assert params  # We expect some params to be generated
    sql = sql % tuple(params)

    # This would be a real query
    query = User.objects.filter(RawSQL(sql, params)).exists()
    
    assert query == (path in user.profile_data)