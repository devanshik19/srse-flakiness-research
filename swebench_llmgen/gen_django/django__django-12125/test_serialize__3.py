import pytest
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSerializer

class TestBaseSerializer(BaseSerializer):
    def serialize(self):
        return "Serialized data"

def test_serialize_not_implemented():
    with pytest.raises(NotImplementedError, match='Subclasses of BaseSerializer must implement the serialize() method.'):
        BaseSerializer().serialize()

def test_serialize_implemented():
    serializer = TestBaseSerializer(value=None)
    serialized_data = serializer.serialize()
    assert serialized_data == "Serialized data"