import copy
import inspect
from importlib import import_module
from django.db import router
from django.db.models.manager import BaseManager
from django.contrib.auth.models import User
import pytest

class TestBaseManager:
    
    def test_check(self):
        # Create an instance of BaseManager
        manager = BaseManager()
        
        # Call the check method with no arguments
        result = manager.check()
        
        # Assert that the result is an empty list
        assert result == []

        # Check that passing arbitrary keyword arguments still returns an empty list
        result_with_kwargs = manager.check(foo='bar', baz='qux')
        assert result_with_kwargs == []