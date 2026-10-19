import pytest
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import ForeignKey
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor

class TestModel(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)

def test_get_prefetch_queryset():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    test_model_instance1 = TestModel.objects.create(user=user1)
    test_model_instance2 = TestModel.objects.create(user=user2)
    
    descriptor = ForwardManyToOneDescriptor(field=TestModel._meta.get_field('user'))
    
    # Test when queryset is None
    queryset, rel_obj_attr, instance_attr, _, cache_name, _ = descriptor.get_prefetch_queryset([test_model_instance1, test_model_instance2])
    
    assert queryset.count() == 2
    assert rel_obj_attr(test_model_instance1) == user1.pk
    assert rel_obj_attr(test_model_instance2) == user2.pk
    
    # Test when queryset is provided
    provided_queryset = User.objects.filter(username__in=['user1', 'user2'])
    queryset, rel_obj_attr, instance_attr, _, cache_name, _ = descriptor.get_prefetch_queryset([test_model_instance1, test_model_instance2], queryset=provided_queryset)
    
    assert queryset.count() == 2
    
    # Verify that users are correctly set in the cache
    for instance in [test_model_instance1, test_model_instance2]:
        related_user = rel_obj_attr(queryset.get(pk=instance.user_id))
        assert related_user == instance.user