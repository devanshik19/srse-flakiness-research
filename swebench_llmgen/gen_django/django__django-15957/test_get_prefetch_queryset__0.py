import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey

class ForwardManyToOneDescriptor:
    def __init__(self, field_with_rel):
        self.field = field_with_rel

    def get_queryset(self):
        return self.field.related_model.objects.all()

    def get_prefetch_queryset(self, instances, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset._add_hints(instance=instances[0])

        rel_obj_attr = self.field.get_foreign_related_value
        instance_attr = self.field.get_local_related_value
        instances_dict = {instance_attr(inst): inst for inst in instances}
        related_field = self.field.foreign_related_fields[0]
        remote_field = self.field.remote_field

        if remote_field.is_hidden() or len(self.field.foreign_related_fields) == 1:
            query = {f"{related_field.name}__in": {instance_attr(inst)[0] for inst in instances}}
        else:
            query = {f"{self.field.related_query_name()}__in": instances}
        queryset = queryset.filter(**query)

        if not remote_field.multiple:
            for rel_obj in queryset:
                instance = instances_dict[rel_obj_attr(rel_obj)]
                remote_field.set_cached_value(rel_obj, instance)
        return (
            queryset,
            rel_obj_attr,
            instance_attr,
            True,
            self.field.get_cache_name(),
            False,
        )

# Test for the `get_prefetch_queryset` method

def test_get_prefetch_queryset():
    class TestModel(models.Model):
        user = ForeignKey(User, on_delete=models.CASCADE, related_name='test_models')

    User.objects.create(username='user1')
    User.objects.create(username='user2')
    instance1 = TestModel.objects.create(user=User.objects.get(username='user1'))
    instance2 = TestModel.objects.create(user=User.objects.get(username='user2'))
    
    field = TestModel._meta.get_field('user')
    descriptor = ForwardManyToOneDescriptor(field)

    queryset, rel_obj_attr, instance_attr, is_cached, cache_name, _ = descriptor.get_prefetch_queryset([instance1, instance2])

    assert queryset.count() == 2
    assert rel_obj_attr(instance1) in [obj.id for obj in queryset]
    assert rel_obj_attr(instance2) in [obj.id for obj in queryset]