import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.utils.functional import cached_property

class RelatedModel(models.Model):
    username = models.CharField(max_length=150, unique=True)

class TestForeignObjectRel(ForeignObjectRel):
    related_model = RelatedModel

@pytest.fixture
def related_model_instance():
    return RelatedModel.objects.create(username='testuser')

@pytest.fixture
def foreign_object_rel():
    return TestForeignObjectRel(
        field=None, 
        to='RelatedModel', 
        related_name='related_set', 
        related_query_name='related_query', 
        limit_choices_to=None, 
        parent_link=False, 
        on_delete=models.CASCADE
    )

def test_get_choices_with_blank(foreign_object_rel, related_model_instance):
    choices = foreign_object_rel.get_choices()
    assert choices[0] == (BLANK_CHOICE_DASH, '')
    assert choices[1] == (related_model_instance.pk, str(related_model_instance))

def test_get_choices_without_blank(foreign_object_rel, related_model_instance):
    choices = foreign_object_rel.get_choices(include_blank=False)
    assert choices == [(related_model_instance.pk, str(related_model_instance))]

def test_get_choices_with_ordering(foreign_object_rel, related_model_instance):
    RelatedModel.objects.create(username='alice')
    RelatedModel.objects.create(username='bob')
    choices = foreign_object_rel.get_choices(ordering=['username'])
    
    assert choices[0] == (BLANK_CHOICE_DASH, '')
    assert choices[1][1] == 'alice'
    assert choices[2][1] == 'bob'