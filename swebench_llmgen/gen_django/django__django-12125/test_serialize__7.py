import pytest
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSerializer


class TestBaseSerializer(BaseSerializer):
    def serialize(self):
        return {'value': self.value}


def test_serialize_not_implemented():
    # Test instantiation of BaseSerializer
    with pytest.raises(NotImplementedError):
        serializer = BaseSerializer()
        serializer.serialize()


def test_test_base_serializer_serialize():
    # Test the TestBaseSerializer's serialization
    serializer = TestBaseSerializer(value='test_value')
    
    result = serializer.serialize()
    
    assert result == {'value': 'test_value'}