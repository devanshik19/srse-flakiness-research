import pytest
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User

class TestBaseSequenceSerializer:
    
    def test_format_not_implemented(self):
        # Create an instance of a subclass that does not implement _format
        class IncompleteSerializer(BaseSequenceSerializer):
            def serialize(self):
                return {}

        serializer = IncompleteSerializer()
        
        with pytest.raises(NotImplementedError, match='Subclasses of BaseSequenceSerializer must implement the _format() method.'):
            serializer._format()