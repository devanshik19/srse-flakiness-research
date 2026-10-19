import pytest
from django.contrib.auth.models import User
from django.db.models.fields import Field


class TestField:
    @pytest.fixture
    def field1(self):
        return Field()

    @pytest.fixture
    def field2(self):
        return Field()

    @pytest.fixture
    def field3(self):
        return Field()

    def test_lt_creation_counter_diff(self, field1, field2):
        field1.creation_counter = 1
        field2.creation_counter = 2
        assert field1 < field2

    def test_lt_creation_counter_equal_no_model(self, field1, field2):
        field1.creation_counter = 1
        field2.creation_counter = 1
        assert not (field1 < field2)
        assert not (field2 < field1)

    def test_lt_creation_counter_equal_with_model(self, field1, field3):
        field1.creation_counter = 1
        field1.model = User
        field3.creation_counter = 1
        field3.model = User

        assert not (field1 < field3)
        assert not (field3 < field1)

    def test_lt_model_diff(self, field1, field2):
        field1.creation_counter = 1
        field2.creation_counter = 1
        field1.model = User
        field2.model = User

        assert not (field1 < field2)
        assert not (field2 < field1)

    def test_lt_model_no_model_first(self, field1, field2):
        field1.creation_counter = 1
        field2.creation_counter = 1
        field1.model = None
        field2.model = User

        assert field1 < field2
        assert not (field2 < field1)

    def test_lt_model_comparison(self, field1, field2):
        field1.creation_counter = 1
        field2.creation_counter = 1
        field1.model = User
        field2.model = User

        assert not (field1 < field2)
        assert not (field2 < field1)