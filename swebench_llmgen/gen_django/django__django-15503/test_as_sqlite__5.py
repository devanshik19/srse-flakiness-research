import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.fields.json import HasKeyLookup

@pytest.mark.django_db
def test_as_sqlite():
    # Arrange
    lookup = HasKeyLookup()
    compiler = User.objects.query.get_compiler(connections['default'])
    connection = connections['default']
    
    # Act
    sql = lookup.as_sqlite(compiler, connection)

    # Assert
    expected_sql = "JSON_TYPE(%s, %s) IS NOT NULL"
    assert expected_sql in sql