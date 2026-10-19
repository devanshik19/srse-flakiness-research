import pytest
from django.contrib.auth.models import User
from django.db import models

from django.db.models.manager import BaseManager

class TestBaseManager:

    def test_check_returns_empty_list(self):
        manager = BaseManager()
        result = manager.check()
        assert result == []