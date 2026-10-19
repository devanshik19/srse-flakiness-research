import pytest
from django.contrib.auth.models import User
from django.db.models import Manager

class TestBaseManager:

    def test_check_empty_kwargs(self):
        manager = Manager()  # Using the Django Manager directly
        result = manager.check()
        assert result == []

    def test_check_with_kwargs(self):
        manager = Manager()  # Using the Django Manager directly
        result = manager.check(field1='value1', field2='value2')
        assert result == []