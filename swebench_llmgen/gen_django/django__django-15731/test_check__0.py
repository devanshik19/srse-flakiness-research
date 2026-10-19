import pytest
from django.contrib.auth.models import User
from django.db.models.manager import BaseManager

def test_check_method():
    manager = BaseManager()
    
    # Check that calling check with no arguments returns an empty list
    result = manager.check()
    assert result == []

    # Check that calling check with arbitrary keyword arguments still returns an empty list
    result_with_kwargs = manager.check(param1='value1', param2='value2')
    assert result_with_kwargs == []