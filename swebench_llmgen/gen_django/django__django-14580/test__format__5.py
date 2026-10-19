import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.migrations.serializer import BaseSequenceSerializer

class TestBaseSequenceSerializer(BaseSequenceSerializer):
    def serialize(self):
        return "Serialized"

def test_format_not_implemented():
    serializer = TestBaseSequenceSerializer()
    with pytest.raises(NotImplementedError, match='Subclasses of BaseSequenceSerializer must implement the _format() method.'):
        serializer._format()