import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


class RelatedModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_models')


@pytest.fixture
def user():
    return User.objects.create(username='testuser')


@pytest.fixture
def related_model(user):
    return RelatedModel.objects.create(user=user)


def test_get_prefetch_queryset(user, related_model):
    descriptor = ForwardManyToOneDescriptor(field=related_model._meta.get_field('user'))
    
    # Test with default queryset
    instances = [related_model]
    queryset, rel_obj_attr, instance_attr, _, cache_name, _ = descriptor.get_prefetch_queryset(instances)
    
    assert queryset.count() == 1
    assert rel_obj_attr(related_model) == user.id
    assert instance_attr(related_model) == (related_model.user.id,)
    
    # Test with custom queryset
    custom_queryset = RelatedModel.objects.filter(user=user)
    queryset, rel_obj_attr, instance_attr, _, cache_name, _ = descriptor.get_prefetch_queryset(instances, queryset=custom_queryset)
    
    assert queryset.count() == 1
    
    # Test when the related field is hidden
    related_model.user.related_models.clear()  # Clear the related field
    hidden_descriptor = ForwardManyToOneDescriptor(field=related_model._meta.get_field('user'))
    queryset, rel_obj_attr, instance_attr, _, cache_name, _ = hidden_descriptor.get_prefetch_queryset(instances)
    
    assert queryset.count() == 0