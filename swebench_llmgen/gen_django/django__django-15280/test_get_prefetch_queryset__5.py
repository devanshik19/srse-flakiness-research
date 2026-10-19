import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey

# A simple model to test against
class Profile(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)

class ForwardManyToOneDescriptor:
    def __init__(self, field_with_rel):
        self.field = field_with_rel

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
    # Setup: Create test instances
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    profile1 = Profile.objects.create(user=user1)
    profile2 = Profile.objects.create(user=user2)

    # Get descriptor
    descriptor = ForwardManyToOneDescriptor(Profile._meta.get_field('user'))

    # Case 1: Get queryset without providing one
    queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor.get_prefetch_queryset([profile1, profile2])

    assert queryset.count() == 2
    assert rel_obj_attr(profile1.user) == user1
    assert rel_obj_attr(profile2.user) == user2

    # Case 2: Get queryset with provided queryset which filters
    queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor.get_prefetch_queryset([profile1], Profile.objects.all())

    assert queryset.count() == 1
    assert rel_obj_attr(profile1.user) == user1

    # Additional Case: Check handling of hidden field (using a dummy hidden field)
    hidden_field = Profile._meta.get_field('user')
    hidden_field.remote_field.is_hidden = lambda: True
    descriptor_with_hidden = ForwardManyToOneDescriptor(hidden_field)

    queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor_with_hidden.get_prefetch_queryset([profile1, profile2])

    assert queryset.count() == 2

    # Ensure that we handle related_query_name on the queryset
    related_field = hidden_field.foreign_related_fields[0]
    assert related_field.related_query_name() == 'profile_set'