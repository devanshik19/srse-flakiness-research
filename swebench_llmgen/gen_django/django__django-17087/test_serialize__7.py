import pytest
from django.contrib.auth.models import User
from django.db import models

class TestBaseSerializer(BaseSerializer):
    def serialize(self):
        return "Serialized data"

def test_base_serializer_raises_not_implemented_error():
    with pytest.raises(NotImplementedError, match="Subclasses of BaseSerializer must implement the serialize() method."):
        serializer = BaseSerializer()
        serializer.serialize()

def test_test_base_serializer_serialize():
    serializer = TestBaseSerializer()
    result = serializer.serialize()
    assert result == "Serialized data"