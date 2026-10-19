import pytest
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor

class RelatedModel:
    def __init__(self, user):
        self.user = user


class TestForwardManyToOneDescriptor:

    @pytest.fixture
    def setup_users(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        return user1, user2

    @pytest.fixture
    def setup_relations(self, setup_users):
        user1, user2 = setup_users
        rel_model = RelatedModel(user1)
        return rel_model, user1, user2
        
    @pytest.fixture
    def descriptor_fixture(self):
        class Field:
            def __init__(self):
                self.foreign_related_fields = [ForeignKey(User, on_delete=None)]
                self.remote_field = self.foreign_related_fields[0]
                self.related_query_name = lambda: 'relatedmodel'
                self.get_foreign_related_value = lambda obj: (obj.user,)
                self.get_local_related_value = lambda obj: (obj.user.id,)
                self.get_cache_name = lambda: 'relatedmodel_cache'

        return ForwardManyToOneDescriptor(Field())

    def test_get_prefetch_queryset(self, setup_relations, descriptor_fixture):
        rel_model, user1, user2 = setup_relations
        queryset = [user1, user2]
        
        result = descriptor_fixture.get_prefetch_queryset([rel_model], queryset)
        
        assert isinstance(result, tuple)
        assert len(result) == 5
        assert isinstance(result[0], list)
        assert user1 in result[0]  # Check if user1 is in the queryset
        assert user2 in result[0]  # Check if user2 is in the queryset
        
    def test_get_prefetch_queryset_no_queryset(self, setup_relations, descriptor_fixture):
        rel_model, user1, _ = setup_relations
        result = descriptor_fixture.get_prefetch_queryset([rel_model])
        
        assert isinstance(result, tuple)
        assert len(result) == 5
        assert isinstance(result[0], list)
        # Check if user1 is in the automatically fetched queryset
        assert user1 in result[0]