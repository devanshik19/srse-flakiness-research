import pytest
from django.contrib.auth.models import User
from django.db.models.fields.related_lookups import RelatedIn

def test_get_prep_lookup_single_column_relation():
    lhs = User._meta.get_field('username')
    rhs = User.objects.filter(username__in=['testuser', 'admin'])

    related_in = RelatedIn(lhs, rhs)
    result = related_in.get_prep_lookup()

    assert result == super(RelatedIn, related_in).get_prep_lookup()

def test_get_prep_lookup_multi_col_relation():
    lhs = User._meta.get_field('username')
    rhs = User.objects.filter(username__in=['testuser']).values('id')

    related_in = RelatedIn(lhs, rhs)
    result = related_in.get_prep_lookup()

    assert result == super(RelatedIn, related_in).get_prep_lookup()

def test_get_prep_lookup_primary_key_condition():
    lhs = User._meta.get_field('username')
    rhs = User.objects.none()

    related_in = RelatedIn(lhs, rhs)
    result = related_in.get_prep_lookup()

    assert result == super(RelatedIn, related_in).get_prep_lookup()