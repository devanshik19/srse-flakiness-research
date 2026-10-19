import pytest
from django.contrib.auth.models import User
from django.db.models import ForeignKey, ManyToManyField
from django.db import models
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


class UserProfile(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='profile')


class TestForwardManyToOneDescriptor:
    
    @pytest.fixture
    def setup_users(self, db):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')
        self.user_profile1 = UserProfile.objects.create(user=self.user1)
        self.user_profile2 = UserProfile.objects.create(user=self.user2)
        self.user_profile3 = UserProfile.objects.create(user=self.user3)

    @pytest.fixture
    def forward_descriptor(self):
        field_with_rel = UserProfile._meta.get_field('user')
        return ForwardManyToOneDescriptor(field_with_rel)

    def test_get_prefetch_queryset_no_queryset(self, setup_users, forward_descriptor):
        instances = [self.user_profile1, self.user_profile2]
        queryset, rel_obj_attr, instance_attr, _, cache_name, _ = forward_descriptor.get_prefetch_queryset(instances)

        assert queryset.count() == 2
        assert set(rel_obj_attr(inst) for inst in queryset) == {self.user1.id, self.user2.id}
        assert cache_name == 'user_id'

    def test_get_prefetch_queryset_with_queryset(self, setup_users, forward_descriptor):
        instances = [self.user_profile1, self.user_profile2]
        custom_queryset = UserProfile.objects.filter(user__username='user1')
        queryset, rel_obj_attr, instance_attr, _, cache_name, _ = forward_descriptor.get_prefetch_queryset(instances, custom_queryset)

        assert queryset.count() == 1
        assert rel_obj_attr(queryset.first()) == self.user1.id
        assert cache_name == 'user_id'

    def test_get_prefetch_queryset_hidden_remote_field(self, setup_users, forward_descriptor):
        UserProfile._meta.get_field('user').remote_field._hidden = True
        instances = [self.user_profile1, self.user_profile2]
        queryset, rel_obj_attr, instance_attr, _, cache_name, _ = forward_descriptor.get_prefetch_queryset(instances)

        assert queryset.count() == 2
        assert set(rel_obj_attr(inst) for inst in queryset) == {self.user1.id, self.user2.id}
        assert cache_name == 'user_id'

    def test_get_prefetch_queryset_multiple_foreign_related_fields(self, setup_users, forward_descriptor):
        UserProfile._meta.get_field('user').foreign_related_fields = [UserProfile._meta.get_field('user')] * 2  # Simulate multiple foreign related fields
        instances = [self.user_profile1, self.user_profile2]
        queryset, rel_obj_attr, instance_attr, _, cache_name, _ = forward_descriptor.get_prefetch_queryset(instances)

        assert queryset.count() == 2
        assert set(rel_obj_attr(inst) for inst in queryset) == {self.user1.id, self.user2.id}
        assert cache_name == 'user_id'