import pytest
from django.contrib.auth.models import User
from django.db.models import Manager

class TestBaseManager:
    @pytest.fixture
    def manager(self):
        return Manager()

    def test_check_method_empty(self, manager):
        result = manager.check()
        assert result == []
        
    def test_check_method_with_kwargs(self, manager):
        result = manager.check(id=1, username='testuser')
        assert result == []