import pytest
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSerializer

class TestBaseSerializer(BaseSerializer):
    def serialize(self):
        return "SerializedData"

def test_serialize_raises_not_implemented():
    with pytest.raises(NotImplementedError, match="Subclasses of BaseSerializer must implement the serialize() method."):
        BaseSerializer().serialize()

def test_test_base_serializer_serialize():
    serializer = TestBaseSerializer(value=None)
    result = serializer.serialize()
    assert result == "SerializedData"