import json
import pytest
from django.db.models import Lookups
from django.contrib.auth.models import User
from django.db.models.fields.json import HasKeyLookup

class TestHasKeyLookup:

    def test_as_sqlite(self):
        # Arrange
        lookup = HasKeyLookup()
        compiler = None  # Replace with an actual compiler instance if needed
        connection = None  # Replace with an actual connection instance if needed

        # Act
        sql_string = lookup.as_sqlite(compiler, connection)

        # Assert
        assert sql_string == "JSON_TYPE(%s, %s) IS NOT NULL"