import pytest
from django.contrib.auth.models import User
from django.db import migrations
from .operations.fields import AddField

class TestAddField:

    @pytest.fixture
    def add_field_instance(self):
        return AddField(model_name='User', name='new_field', field=None, preserve_default=NOT_PROVIDED)

    def test_migration_name_fragment(self, add_field_instance):
        result = add_field_instance.migration_name_fragment()
        expected = "user_new_field"
        assert result == expected