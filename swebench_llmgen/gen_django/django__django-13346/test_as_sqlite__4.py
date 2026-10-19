import pytest
from django.db.models import ExpressionWrapper, F
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.db.models.lookups import HasKeyLookup

@pytest.mark.django_db
def test_as_sqlite():
    # Set up a simple JSON field in a User model
    User.objects.create(username='user1', data={'key1': 'value1', 'key2': 'value2'})
    
    # Create an ExpressionWrapper using the JSONField and invoke the HasKeyLookup
    json_field = JSONField()
    lookup = HasKeyLookup()
    
    # Prepare the compiler and connection mocks
    class MockCompiler:
        pass
    
    class MockConnection:
        pass

    # Create fake compiler and connection
    compiler = MockCompiler()
    connection = MockConnection()
    
    # Execute the as_sqlite method
    sql = lookup.as_sqlite(compiler, connection)

    # Validate that the generated SQL matches the expected format
    expected_template = 'JSON_TYPE(%s, %s) IS NOT NULL'
    assert sql == expected_template