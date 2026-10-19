import pytest
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSerializer


class TestBaseSerializer(BaseSerializer):
    def serialize(self):
        return "This is a serialized string."


def test_serialize_not_implemented():
    with pytest.raises(NotImplementedError):
        serializer = BaseSerializer()
        serializer.serialize()


def test_serialize_implemented():
    serializer = TestBaseSerializer(value="test")
    result = serializer.serialize()
    assert result == "This is a serialized string."