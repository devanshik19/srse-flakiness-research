import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.core import exceptions
from django.utils.functional import cached_property

class TestForeignObjectRel:
    @pytest.fixture
    def foreign_object_rel(self):
        # Initialize a ForeignObjectRel with a User model as related_model
        rel = ForeignObjectRel(
            field=None,
            to=User,
            related_name='test_related',
            related_query_name='test_related_q',
            limit_choices_to=None,
            parent_link=False,
            on_delete=models.CASCADE
        )
        return rel

    def test_get_choices_with_blank(self, foreign_object_rel):
        # Ensure that choices include a blank option
        choices = foreign_object_rel.get_choices(include_blank=True)
        assert choices[0] == (BLANK_CHOICE_DASH, '')  # Check blank choice at the start
        assert len(choices) == 1 + User.objects.count()  # One for blank + users

    def test_get_choices_without_blank(self, foreign_object_rel):
        # Ensure that choices do not include a blank option
        choices = foreign_object_rel.get_choices(include_blank=False)
        assert choices == [(user.pk, str(user)) for user in User.objects.order_by()]
        assert BLANK_CHOICE_DASH not in [choice[0] for choice in choices]

    def test_get_choices_with_ordering(self, foreign_object_rel):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        choices = foreign_object_rel.get_choices(ordering=['username'])
        assert choices[1][0] == user1.pk  # Ensure correct ordering by username
        assert choices[2][0] == user2.pk  # User2 should be after user1