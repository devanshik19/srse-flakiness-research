import pytest
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSerializer

class TestBaseSerializer:

    def test_serialize_not_implemented(self):
        serializer = BaseSerializer()
        with pytest.raises(NotImplementedError, match="Subclasses of BaseSerializer must implement the serialize() method."):
            serializer.serialize()