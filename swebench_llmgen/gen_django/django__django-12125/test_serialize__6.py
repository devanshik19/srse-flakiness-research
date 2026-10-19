import pytest
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSerializer

class TestBaseSerializer(BaseSerializer):
    def serialize(self):
        return 'Serialized Data'

def test_serialize_not_implemented():
    with pytest.raises(NotImplementedError):
        base_serializer = BaseSerializer()
        base_serializer.serialize()

def test_test_base_serializer_serialize():
    test_serializer = TestBaseSerializer(value=None)
    result = test_serializer.serialize()
    assert result == 'Serialized Data'