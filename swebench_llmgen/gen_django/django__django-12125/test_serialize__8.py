import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.serializer import BaseSerializer

class TestBaseSerializer(BaseSerializer):
    def __init__(self, value):
        super().__init__(value)

    def serialize(self):
        return f"Serialized: {self.value}"

def test_base_serializer_serialize():
    # Arrange
    user = User(username='testuser')
    user.save()
    
    # Act
    serializer = TestBaseSerializer(user)
    
    # Assert
    with pytest.raises(NotImplementedError) as excinfo:
        serializer.serialize()
    assert str(excinfo.value) == 'Subclasses of BaseSerializer must implement the serialize() method.'