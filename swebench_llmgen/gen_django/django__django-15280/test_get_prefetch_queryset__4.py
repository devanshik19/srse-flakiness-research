import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.db.models import Prefetch

class RelatedExample(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='related_exapmle')

class ForwardManyToOneDescriptor:
    def __init__(self, field_with_rel):
        self.field = field_with_rel

    def get_queryset(self):
        return RelatedExample.objects.all()
    
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
            query = {'%s__in' % related_field.name: {instance_attr(inst)[0] for inst in instances}}
        else:
            query = {'%s__in' % self.field.related_query_name(): instances}
        queryset = queryset.filter(**query)

        if not remote_field.multiple:
            for rel_obj in queryset:
                instance = instances_dict[rel_obj_attr(rel_obj)]
                remote_field.set_cached_value(rel_obj, instance)
        return queryset, rel_obj_attr, instance_attr, True, self.field.get_cache_name(), False

@pytest.mark.django_db
def test_get_prefetch_queryset():
    user1 = User.objects.create_user(username='user1')
    user2 = User.objects.create_user(username='user2')

    rel1 = RelatedExample.objects.create(user=user1)
    rel2 = RelatedExample.objects.create(user=user2)

    descriptor = ForwardManyToOneDescriptor(User._meta.get_field('related_exapmle'))
    queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor.get_prefetch_queryset([user1, user2])

    assert queryset.count() == 2
    assert rel_obj_attr(rel1) == user1
    assert rel_obj_attr(rel2) == user2