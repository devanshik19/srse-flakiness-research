import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.db.models.fields.related import RelatedField

class TestRelatedField:
    @pytest.fixture
    def related_field(self):
        return RelatedField(related_name='related_user', related_query_name='related_user_qs', limit_choices_to=None)

    def test_db_type_returns_none(self, related_field):
        assert related_field.db_type(connection) is None