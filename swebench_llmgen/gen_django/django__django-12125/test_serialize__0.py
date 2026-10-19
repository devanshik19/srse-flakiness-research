import pytest
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSerializer

class TestBaseSerializer(BaseSerializer):

    def serialize(self):
        return "Serialized Data"

def test_serialize_raises_notimplementederror():
    with pytest.raises(NotImplementedError, match='Subclasses of BaseSerializer must implement the serialize() method.'):
        serializer = BaseSerializer()
        serializer.serialize()

def test_serialize_implemented_method():
    test_serializer = TestBaseSerializer(value="test_value")
    result = test_serializer.serialize()
    assert result == "Serialized Data"