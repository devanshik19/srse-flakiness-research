import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, Manager
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor

class RelatedModel(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='related_models')

class TestForwardManyToOneDescriptor:

    @pytest.fixture
    def setup_users_and_related_models(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        RelatedModel.objects.create(user=user1)
        RelatedModel.objects.create(user=user1)
        RelatedModel.objects.create(user=user2)
        return user1, user2

    def test_get_prefetch_queryset_no_queryset(self, setup_users_and_related_models):
        user1, user2 = setup_users_and_related_models
        instances = [user1, user2]
        
        descriptor = ForwardManyToOneDescriptor(RelatedModel._meta.get_field('user'))
        queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor.get_prefetch_queryset(instances)

        assert queryset.count() == 3
        assert all(rel.user in instances for rel in queryset)

    def test_get_prefetch_queryset_with_queryset(self, setup_users_and_related_models):
        user1, user2 = setup_users_and_related_models
        instances = [user1]

        descriptor = ForwardManyToOneDescriptor(RelatedModel._meta.get_field('user'))
        predefined_queryset = RelatedModel.objects.filter(user=user1)
        
        queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor.get_prefetch_queryset(instances, predefined_queryset)

        assert queryset.count() == 2
        assert all(rel.user == user1 for rel in queryset)

    def test_get_prefetch_queryset_hidden_field(self, setup_users_and_related_models):
        user1, _ = setup_users_and_related_models
        instances = [user1]

        # Simulating a hidden field by using a related field
        hidden_field = RelatedModel._meta.get_field('user')
        hidden_field._remote_field.set_hidden(True)  # Mark as hidden for testing

        descriptor = ForwardManyToOneDescriptor(hidden_field)
        queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor.get_prefetch_queryset(instances)

        assert queryset.count() == 2
        assert all(rel.user == user1 for rel in queryset)

    def test_get_prefetch_queryset_multiple_relations(self, setup_users_and_related_models):
        user1, user2 = setup_users_and_related_models
        instances = [user1, user2]

        descriptor = ForwardManyToOneDescriptor(RelatedModel._meta.get_field('user'))
        queryset, rel_obj_attr, instance_attr, _, _, _ = descriptor.get_prefetch_queryset(instances)

        assert queryset.count() == 3
        assert all(rel.user in instances for rel in queryset)