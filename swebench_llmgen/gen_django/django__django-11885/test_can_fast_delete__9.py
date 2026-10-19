import pytest
from collections import Counter
from django.contrib.auth.models import User
from django.db import IntegrityError, connections, transaction
from django.db.models import signals
from django.db.models.deletion import Collector

@pytest.fixture
def setup_users():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    return user1, user2

def test_can_fast_delete_no_conditions(setup_users):
    collector = Collector(using='default')
    user1, user2 = setup_users

    result = collector.can_fast_delete(user1)
    assert result is True

def test_can_fast_delete_with_cascade(setup_users):
    collector = Collector(using='default')
    
    class MockField:
        def __init__(self, on_delete):
            self.remote_field = MockRemoteField(on_delete)

    class MockRemoteField:
        def __init__(self, on_delete):
            self.on_delete = on_delete

    user1, user2 = setup_users
    user1._meta = type('Meta', (), {'parents': {}})
    user1._meta.concrete_model = type('Model', (), {'_meta': type('Meta', (), {
        'parents': {},
        'private_fields': [],
    })})

    user1._meta.concrete_model._meta.get_related = lambda _: []
    user1._meta.concrete_model._meta.fields = [MockField(on_delete=Cascade)]
    result = collector.can_fast_delete(user1, from_field=MockField(on_delete=CASCADE))
    assert result is False

def test_can_fast_delete_with_signal_listeners(setup_users):
    collector = Collector(using='default')

    def mock_signal_listener(sender, **kwargs):
        pass
    
    signals.pre_delete.connect(mock_signal_listener)

    user1 = User(username='user1')
    user1._meta = type('Meta', (), {'parents': {}, 'private_fields': []})
    user1._meta.concrete_model = type('Model', (), {
        '_meta': type('Meta', (), {
            'parents': {},
            'private_fields': [],
        })
    })

    result = collector.can_fast_delete(user1)
    assert result is False

    signals.pre_delete.disconnect(mock_signal_listener)

def test_can_fast_delete_parent_child_chain(setup_users):
    collector = Collector(using='default')
    user1, user2 = setup_users

    user1._meta = type('Meta', (), {'parents': {}})
    user2._meta = type('Meta', (), {'parents': {}})
    
    user1._meta.concrete_model = type('Model', (), {'_meta': type('Meta', (), {
        'parents': {user2: 'user1'},
        'private_fields': [],
    })})

    result = collector.can_fast_delete(user1, from_field=None)
    assert result is True

def test_can_fast_delete_invalid_input(collector):
    collector = Collector(using='default')
    result = collector.can_fast_delete(None)
    assert result is False

    result = collector.can_fast_delete('not_a_user')
    assert result is False