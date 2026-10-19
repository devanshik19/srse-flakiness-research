import pytest
from django.contrib.auth.models import User
from django.db import models

class RelatedField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ForwardManyToOneDescriptor:
    def __init__(self, field_with_rel):
        self.field = field_with_rel

    def get_queryset(self):
        return User.objects.all()  # Simplified queryset for testing purpose

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
            query = {
                "%s__in" % related_field.name: {instance_attr(inst)[0] for inst in instances}
            }
        else:
            query = {"%s__in" % self.field.related_query_name(): instances}
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

@pytest.mark.django_db
def test_get_prefetch_queryset():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    class ForeignRelatedField:
        def __init__(self, name):
            self.name = name
            self.foreign_related_fields = [self]
            self.remote_field = self
            self.model = User

        def is_hidden(self):
            return False

        def get_foreign_related_value(self, instance):
            return instance.id

        def get_local_related_value(self, instance):
            return instance.id

        def related_query_name(self):
            return self.name

        def get_cache_name(self):
            return 'related_cache'

        def set_cached_value(self, rel_obj, instance):
            pass

    field = ForeignRelatedField('user_id')

    descriptor = ForwardManyToOneDescriptor(field)

    # Test with default queryset
    queryset, *rest = descriptor.get_prefetch_queryset([user1, user2])
    assert queryset.count() == 2

    # Test with a custom queryset
    custom_queryset = User.objects.filter(username='user1')
    queryset, *rest = descriptor.get_prefetch_queryset([user1, user2], queryset=custom_queryset)
    assert queryset.count() == 1

    # Test with hidden field
    field.remote_field.is_hidden = lambda: True
    queryset, *rest = descriptor.get_prefetch_queryset([user1, user2])
    assert queryset.count() == 2

    # Ensure the parameters returned are as expected
    assert rest[0] == field.get_foreign_related_value
    assert rest[1] == field.get_local_related_value
    assert rest[2] is True
    assert rest[3] == field.get_cache_name()
    assert rest[4] is False