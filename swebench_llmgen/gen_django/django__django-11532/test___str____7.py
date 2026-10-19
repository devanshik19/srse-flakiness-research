import socket
import pytest
from django.contrib.auth.models import User
from django.core.mail.utils import CachedDnsName

@pytest.fixture
def cached_dns_name():
    # Assuming the get_fqdn method is to return the FQDN of the user for the test
    dns_name = CachedDnsName()
    dns_name.get_fqdn = lambda: f"{socket.gethostname()}.example.com"
    return dns_name

def test_str_method(cached_dns_name):
    expected_fqdn = f"{socket.gethostname()}.example.com"
    assert str(cached_dns_name) == expected_fqdn