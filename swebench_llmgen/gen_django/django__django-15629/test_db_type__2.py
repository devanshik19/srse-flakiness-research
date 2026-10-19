import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.fields.related import RelatedField

class TestRelatedField:
    def setup_method(self):
        self.field = RelatedField(related_name='related_user', related_query_name='related_query', limit_choices_to=None)
    
    def test_db_type_returns_none(self):
        connection = connections['default']
        assert self.field.db_type(connection) is None