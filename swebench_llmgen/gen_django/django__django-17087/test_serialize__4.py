import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

from django.db.migrations.serializer import BaseSerializer

class TestBaseSerializer(BaseSerializer):
    def serialize(self):
        return "Serialized Data"

def test_serialize_method_implemented():
    serializer = TestBaseSerializer(value=None)
    assert serializer.serialize() == "Serialized Data"

def test_base_serializer_raises_not_implemented_error():
    with pytest.raises(NotImplementedError, match="Subclasses of BaseSerializer must implement the serialize() method."):
        BaseSerializer(value=None).serialize()