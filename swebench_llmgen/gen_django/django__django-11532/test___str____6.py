import pytest
from django.contrib.auth.models import User
from django.core.mail.utils import CachedDnsName

@pytest.fixture
def cached_dns_name():
    # Create a CachedDnsName instance
    instance = CachedDnsName()
    return instance

def test_str_returns_fqdn(mocker, cached_dns_name):
    # Mock the get_fqdn method to return a specific value
    mocker.patch.object(cached_dns_name, 'get_fqdn', return_value='mocked.fqdn.com')
    
    # Call the __str__ method
    result = str(cached_dns_name)
    
    # Assert that the returned string is the mocked fqdn
    assert result == 'mocked.fqdn.com'

def test_str_calls_get_fqdn(cached_dns_name, mocker):
    # Mock the get_fqdn method
    get_fqdn_mock = mocker.patch.object(cached_dns_name, 'get_fqdn', return_value='another.mocked.fqdn.com')
    
    # Call the __str__ method
    _ = str(cached_dns_name)
    
    # Assert that get_fqdn was called
    get_fqdn_mock.assert_called_once()