import datetime
import decimal
from importlib import import_module
import sqlparse
from django.conf import settings
from django.db import NotSupportedError, transaction
from django.db.backends import utils
from django.utils import timezone
from django.utils.encoding import force_str
import pytest
from django.contrib.auth.models import User
from django.db.backends.base.operations import BaseDatabaseOperations

@pytest.mark.parametrize("input_value,expected_output", [
    (None, None),
    ("192.168.0.1", "192.168.0.1"),
    ("255.255.255.255", "255.255.255.255"),
    ("", None),
])
def test_adapt_ipaddressfield_value(input_value, expected_output):
    db_operations = BaseDatabaseOperations()
    result = db_operations.adapt_ipaddressfield_value(input_value)
    assert result == expected_output