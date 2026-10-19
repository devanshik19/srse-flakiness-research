import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.db.models.sql.query import Query
from django.db.models import ForeignKey, Model

class RelatedModel(Model):
    user = ForeignKey(User, on_delete=models.CASCADE)

def test_check_related_objects_invalid_queryset():
    user_queryset = User.objects.all()
    query = Query(model=RelatedModel, where=None, alias_cols=False)
    
    with pytest.raises(ValueError, match="Cannot use QuerySet for"):
        query.check_related_objects(RelatedModel._meta.get_field('user'), user_queryset, RelatedModel._meta)

def test_check_related_objects_valid_instance():
    user = User.objects.create(username='testuser')
    query = Query(model=RelatedModel, where=None, alias_cols=False)
    
    # Check with a valid instance
    query.check_related_objects(RelatedModel._meta.get_field('user'), user, RelatedModel._meta)

def test_check_related_objects_iterable_of_instances():
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    query = Query(model=RelatedModel, where=None, alias_cols=False)
    
    # Check with an iterable of valid instances
    query.check_related_objects(RelatedModel._meta.get_field('user'), [user1, user2], RelatedModel._meta)

def test_check_related_objects_invalid_instance():
    user = User.objects.create(username='testuser')
    invalid_user = 'Invalid User'
    query = Query(model=RelatedModel, where=None, alias_cols=False)

    with pytest.raises(ValueError):
        query.check_related_objects(RelatedModel._meta.get_field('user'), invalid_user, RelatedModel._meta)