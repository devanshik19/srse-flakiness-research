import pytest
from django.contrib.auth.models import User
from django.db.models import ForeignKey, Manager
from django.db import models

class RelatedModel(models.Model):
    user = ForeignKey(User, related_name='related_models', on_delete=models.CASCADE)

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
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    related_instance1 = RelatedModel.objects.create(user=user1)
    related_instance2 = RelatedModel.objects.create(user=user1)
    related_instance3 = RelatedModel.objects.create(user=user2)

    descriptor = ForwardManyToOneDescriptor(related_instance1._meta.get_field('user'))
    
    # Test retrieving queryset for multiple instances
    queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor.get_prefetch_queryset(
        [related_instance1, related_instance2]
    )
    
    assert queryset.count() == 2
    assert set(queryset) == {related_instance1, related_instance2}

    # Test retrieving queryset for a single user with hidden field
    related_instance1._meta.get_field('user').remote_field.set_hidden()  # Simulate hidden field
    queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor.get_prefetch_queryset(
        [related_instance1]
    )
    
    assert queryset.count() == 1
    assert queryset.first() == related_instance1

    # Test instances dict mapping
    instances_dict = {instance_attr(inst): inst for inst in [related_instance1, related_instance2]}
    assert related_instance1 in instances_dict.values()
    assert related_instance2 in instances_dict.values()