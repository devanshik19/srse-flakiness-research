import pytest
from django.db.migrations.serializer import BaseSequenceSerializer

class TestBaseSequenceSerializer:

    def test_format_not_implemented(self):
        serializer = BaseSequenceSerializer()

        with pytest.raises(NotImplementedError, match='Subclasses of BaseSequenceSerializer must implement the _format() method.'):
            serializer._format()