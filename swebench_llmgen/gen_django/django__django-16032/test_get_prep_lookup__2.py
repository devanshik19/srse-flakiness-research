import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.fields.related_lookups import RelatedIn

class TestRelatedIn:
    @pytest.fixture
    def setup_related_in(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        return RelatedIn(), user1, user2

    def test_get_prep_lookup_single_column_relation(self, setup_related_in):
        related_in, user1, user2 = setup_related_in
        related_in.lhs = user1.__class__._meta.get_field('username')
        related_in.rhs = ['user1', 'user2']

        result = related_in.get_prep_lookup()
        assert result is not None
        assert related_in.rhs == ['user1', 'user2']

    def test_get_prep_lookup_with_primary_key(self, setup_related_in):
        related_in, user1, user2 = setup_related_in
        related_in.lhs = user1.__class__._meta.get_field('id')
        related_in.rhs = [user1.id, user2.id]

        result = related_in.get_prep_lookup()
        assert result is not None
        assert related_in.rhs == [user1.id, user2.id]

    def test_get_prep_lookup_no_select_fields(self, setup_related_in):
        related_in, user1, user2 = setup_related_in
        related_in.lhs = user1.__class__._meta.get_field('username')
        related_in.rhs = ['user1']

        # Simulate the behavior to set has_select_fields to False
        related_in.rhs.has_select_fields = False

        with pytest.raises(AttributeError):
            related_in.get_prep_lookup()

    def test_get_prep_lookup_multi_column_source(self, setup_related_in):
        related_in, user1, user2 = setup_related_in
        related_in.lhs = user1.__class__._meta.get_field('username')  # Not a MultiColSource
        related_in.rhs = ['user1', "user2"]
        related_in.rhs_is_direct_value = lambda: True  # Simulating direct value case

        result = related_in.get_prep_lookup()
        assert result is not None
        assert related_in.rhs == ['user1', 'user2']