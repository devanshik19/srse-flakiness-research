import pytest
from django.contrib.auth.models import User
from django.db import models

class BaseManager(models.Manager):
    def check(self, **kwargs):
        return []

def test_base_manager_check():
    manager = BaseManager()
    result = manager.check(some_arg='test')
    
    # Check that the result is an empty list
    assert result == []
    
    # Check that it can be called with no arguments
    result_no_args = manager.check()
    assert result_no_args == []
    
    # Test with different keyword arguments
    result_with_keywords = manager.check(arg1='value1', arg2='value2')
    assert result_with_keywords == []