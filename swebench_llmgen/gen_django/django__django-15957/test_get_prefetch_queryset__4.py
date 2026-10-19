import pytest
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import FieldError

class ForeignKeyField(models.ForeignKey):
    pass

class TestForwardManyToOneDescriptor:
    @pytest.fixture
    def setup(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')
        self.model = self.create_related_model()
        self.field = ForeignKeyField(User, related_name='related_model_set')
        self.descriptor = ForwardManyToOneDescriptor(self.field)

    def create_related_model(self):
        class RelatedModel(models.Model):
            user = ForeignKeyField(User, on_delete=models.CASCADE)

        return RelatedModel

    def test_get_prefetch_queryset_no_queryset(self, setup):
        instances = [self.user1, self.user2]
        queryset, *rest = self.descriptor.get_prefetch_queryset(instances)
        
        assert queryset.count() == 0  # No related models created yet
        
        # Create related objects
        self.model.objects.create(user=self.user1)
        self.model.objects.create(user=self.user2)

        queryset, *rest = self.descriptor.get_prefetch_queryset(instances)
        assert queryset.count() == 2  # Should match the number of related models

    def test_get_prefetch_queryset_with_queryset(self, setup):
        instances = [self.user1]
        related_instance = self.model.objects.create(user=self.user1)

        queryset = self.model.objects.all()
        returned_queryset, *rest = self.descriptor.get_prefetch_queryset(instances, queryset)
        
        assert returned_queryset.count() == 1  # Should only return the related_instance
        
        # Check the instance that was returned
        assert returned_queryset.first() == related_instance

    def test_get_prefetch_queryset_with_hidden_field(self, setup):
        # Simulate hidden field condition
        self.field.remote_field.is_hidden = lambda: True
        instances = [self.user1]

        related_instance = self.model.objects.create(user=self.user1)
        queryset = self.model.objects.all()

        returned_queryset, *rest = self.descriptor.get_prefetch_queryset(instances, queryset)
        
        assert returned_queryset.count() == 1  # Should match the related instance
        assert returned_queryset.first() == related_instance

    def test_get_prefetch_queryset_multiple_related_fields(self, setup):
        # Overriding the related field to simulate multiple fields scenario
        self.field.foreign_related_fields.append(ForeignKeyField(User, related_name='additional_related_model_set'))
        instances = [self.user1, self.user2]

        # Create multiple related models
        related1 = self.model.objects.create(user=self.user1)
        related2 = self.model.objects.create(user=self.user2)
        queryset = self.model.objects.all()

        returned_queryset, *rest = self.descriptor.get_prefetch_queryset(instances, queryset)

        assert returned_queryset.count() == 2  # Should return both related models