import pytest
from django.db.migrations.serializer import BaseSequenceSerializer

class TestBaseSequenceSerializer(BaseSequenceSerializer):
    def serialize(self):
        return "serializing"

def test_format_not_implemented():
    serializer = TestBaseSequenceSerializer()
    with pytest.raises(NotImplementedError, match='Subclasses of BaseSequenceSerializer must implement the _format() method.'):
        serializer._format()