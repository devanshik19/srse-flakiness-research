import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.db.models.lookups import Lookup
from django.utils.translation import gettext_lazy as _
from .lookup import HasKeyLookup

@pytest.mark.django_db
def test_as_sqlite():
    # Create a sample User instance with JSON field
    user = User.objects.create(username='testuser', password='testpassword')
    
    # Create a dummy compiler and connection (mocked representation)
    class MockCompiler:
        def quote_name(self, name):
            return f'"{name}"'

    class MockConnection:
        pass

    compiler = MockCompiler()
    connection = MockConnection()
    
    # Create an instance of HasKeyLookup
    lookup = HasKeyLookup()

    # Call the as_sqlite method
    sql = lookup.as_sqlite(compiler, connection)

    # Verify SQL output matches the expected template
    expected_sql = 'JSON_TYPE(%s, %%s) IS NOT NULL'
    assert sql == expected_sql