import json
import pytest
from django.contrib.auth.models import User
from django.db.models import ExpressionWrapper, F
from django.db.models.fields.json import HasKeyLookup

@pytest.mark.parametrize('key', ['key1', 'key2', 'key3'])
def test_as_sqlite(key):
    # Create a User instance
    user = User.objects.create(username='testuser', email='test@example.com', password='password123')
    
    # Assume that there's a JSONField in User model for the sake of test
    user.profile_data = json.dumps({'key1': 'value1', 'key2': 'value2'})
    user.save()

    # Create an instance of HasKeyLookup
    lookup = HasKeyLookup()
    
    # Use an instance of the compiler and connection (simulated)
    compiler = user._meta.model._default_manager._queryset_class()
    connection = compiler.db
    
    # Call the as_sqlite method
    sql, params = lookup.as_sqlite(compiler, connection)

    # Validate the output SQL and parameters
    expected_sql = f"JSON_TYPE(%s, %s) IS NOT NULL"
    expected_params = [user.profile_data, key]
    
    assert sql == expected_sql
    assert params == expected_params