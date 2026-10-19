import pytest
from django.contrib.auth.models import User
from django.db.models.query_utils import RegisterLookupMixin

class ConcreteRegisterLookup(RegisterLookupMixin):
    class_lookups = {}

@pytest.fixture
def setup_lookup():
    lookup = namedtuple('Lookup', ['lookup_name'])(lookup_name='my_lookup')
    ConcreteRegisterLookup.class_lookups[lookup.lookup_name] = lookup
    return lookup

def test_unregister_lookup_with_name(setup_lookup):
    lookup = setup_lookup
    ConcreteRegisterLookup._unregister_lookup(ConcreteRegisterLookup, lookup)
    assert 'my_lookup' not in ConcreteRegisterLookup.class_lookups

def test_unregister_lookup_without_name(setup_lookup):
    lookup = setup_lookup
    ConcreteRegisterLookup._unregister_lookup(ConcreteRegisterLookup, lookup, lookup_name='my_lookup')
    assert 'my_lookup' not in ConcreteRegisterLookup.class_lookups

def test_unregister_lookup_non_existent(setup_lookup):
    lookup = namedtuple('Lookup', ['lookup_name'])(lookup_name='non_existent_lookup')
    with pytest.raises(KeyError):
        ConcreteRegisterLookup._unregister_lookup(ConcreteRegisterLookup, lookup)