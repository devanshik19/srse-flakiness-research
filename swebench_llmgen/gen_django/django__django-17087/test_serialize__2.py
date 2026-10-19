import pytest
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSerializer

class TestBaseSerializer(BaseSerializer):
    def serialize(self):
        return "Test serialization"

def test_base_serializer_serialize():
    serializer = TestBaseSerializer(value="Test value")
    result = serializer.serialize()
    assert result == "Test serialization"

def test_base_serializer_serialize_not_implemented():
    with pytest.raises(NotImplementedError, match="Subclasses of BaseSerializer must implement the serialize() method."):
        serializer = BaseSerializer(value="Test value")
        serializer.serialize()