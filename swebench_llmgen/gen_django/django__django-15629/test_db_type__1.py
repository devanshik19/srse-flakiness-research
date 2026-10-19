import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Field


class RelatedField(Field):
    def db_type(self, connection):
        # By default related field will not have a column as it relates to
        # columns from another table.
        return None


def test_db_type():
    related_field = RelatedField()
    
    assert related_field.db_type(connection) is None