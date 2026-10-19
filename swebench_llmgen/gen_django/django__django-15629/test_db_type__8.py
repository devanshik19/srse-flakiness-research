import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Field

class RelatedField(Field):

    def __init__(self, related_name=None, related_query_name=None, limit_choices_to=None):
        self.related_name = related_name
        self.related_query_name = related_query_name
        self.limit_choices_to = limit_choices_to

    def db_type(self, connection):
        # By default related field will not have a column as it relates to
        # columns from another table.
        return None

@pytest.mark.parametrize("expected_db_type", [None])
def test_db_type(expected_db_type):
    related_field = RelatedField()
    assert related_field.db_type(connection) == expected_db_type