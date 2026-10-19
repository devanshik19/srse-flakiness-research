import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.utils.functional import cached_property

class TestForeignObjectRel:
    @pytest.fixture
    def user(self):
        return User.objects.create(username='testuser')

    @pytest.fixture
    def foreign_object_rel(self, user):
        class RelatedModel(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)

        # Simulating ForeignObjectRel initialization
        foreign_object = ForeignObjectRel(
            field=None,
            to=RelatedModel,
            related_name='related_user',
            related_query_name='related_user_query',
            limit_choices_to=None,
            parent_link=False,
            on_delete=models.CASCADE
        )
        return foreign_object

    def test_get_choices_includes_blank(self, foreign_object_rel, user):
        # Setup a related instance
        related_instance = foreign_object_rel.related_model.objects.create(user=user)
        
        choices = foreign_object_rel.get_choices()
        assert choices == [('', '---------'), (related_instance.pk, str(related_instance))]

    def test_get_choices_excludes_blank(self, foreign_object_rel, user):
        # Setup a related instance
        related_instance = foreign_object_rel.related_model.objects.create(user=user)
        
        choices = foreign_object_rel.get_choices(include_blank=False)
        assert choices == [(related_instance.pk, str(related_instance))]
        
    def test_get_choices_with_custom_blank_choice(self, foreign_object_rel, user):
        # Setup a related instance
        related_instance = foreign_object_rel.related_model.objects.create(user=user)
        
        custom_blank_choice = ('0', 'No selection')
        choices = foreign_object_rel.get_choices(blank_choice=custom_blank_choice)
        
        assert choices == [custom_blank_choice, (related_instance.pk, str(related_instance))]