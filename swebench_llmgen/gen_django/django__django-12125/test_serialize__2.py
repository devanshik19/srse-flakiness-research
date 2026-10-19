import pytest
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSerializer

class TestBaseSerializer(BaseSerializer):
    def serialize(self):
        return "Serialized BaseSerializer"

def test_serialize():
    serializer = TestBaseSerializer(value=None)
    result = serializer.serialize()
    assert result == "Serialized BaseSerializer"

def test_serialize_not_implemented():
    with pytest.raises(NotImplementedError, match='Subclasses of BaseSerializer must implement the serialize() method.'):
        serializer = BaseSerializer(value=None)
        serializer.serialize()