import pytest
from django.contrib.auth.models import User
from django.db.models import Manager

class BaseManager(Manager):
    def check(self, **kwargs):
        return []

def test_base_manager_check_empty_response():
    # Arrange
    manager = BaseManager()
    
    # Act
    result = manager.check()

    # Assert
    assert isinstance(result, list)
    assert len(result) == 0

def test_base_manager_check_with_kwargs():
    # Arrange
    manager = BaseManager()
    
    # Act
    result = manager.check(param1='value1', param2='value2')

    # Assert
    assert isinstance(result, list)
    assert len(result) == 0