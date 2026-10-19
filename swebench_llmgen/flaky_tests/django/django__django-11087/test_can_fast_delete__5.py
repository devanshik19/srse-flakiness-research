import pytest
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import signals

class Collector:
    def __init__(self, using):
        self.using = using

    def can_fast_delete(self, objs, from_field=None):
        if from_field and from_field.remote_field.on_delete is not CASCADE:
            return False
        if hasattr(objs, '_meta'):
            model = type(objs)
        elif hasattr(objs, 'model') and hasattr(objs, '_raw_delete'):
            model = objs.model
        else:
            return False
        if (signals.pre_delete.has_listeners(model) or
                signals.post_delete.has_listeners(model) or
                signals.m2m_changed.has_listeners(model)):
            return False
        opts = model._meta
        return (
            all(link == from_field for link in opts.concrete_model._meta.parents.values()) and
            all(
                related.field.remote_field.on_delete is DO_NOTHING
                for related in get_candidate_relations_to_delete(opts)
            ) and (
                not any(hasattr(field, 'bulk_related_objects') for field in opts.private_fields)
            )
        )

@pytest.fixture
def collector():
    return Collector(using='default')

def test_can_fast_delete_no_listeners(collector):
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user) is True

def test_can_fast_delete_with_pre_delete_listener(collector):
    def listener(sender, **kwargs):
        pass

    signals.pre_delete.connect(listener, sender=User)
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user) is False
    signals.pre_delete.disconnect(listener, sender=User)

def test_can_fast_delete_with_different_on_delete_behavior(collector):
    from_field = None  # Simulate some field that name does not link to CASCADE
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user, from_field) is False

def test_can_fast_delete_with_bulk_related_objects(collector):
    user = User.objects.create(username='testuser')
    # Simulate a scenario with bulk_related_objects
    User._meta.private_fields.append('some_field_with_bulk_related_objects')
    assert collector.can_fast_delete(user) is False
    User._meta.private_fields.remove('some_field_with_bulk_related_objects')