import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

@pytest.mark.django_db
def test_query_with_deferred_filter():
    user = User.objects.create(username='testuser', password='password')
    qs = User.objects.filter(username='testuser')
    
    # Simulate deferred filter state
    qs._deferred_filter = (False, ('username',), {})
    
    # Call the query method which should apply the deferred filter
    result = qs.query()
    
    # Check that the result is the same as filtering directly
    assert list(result) == list(qs)

@pytest.mark.django_db
def test_query_without_deferred_filter():
    user1 = User.objects.create(username='testuser1', password='password1')
    user2 = User.objects.create(username='testuser2', password='password2')
    qs = User.objects.all()
    
    # Initially, no deferred filter is set
    qs._deferred_filter = None
    
    # Call the query method
    result = qs.query()
    
    # Check that the result includes all users
    assert len(list(result)) == 2
    assert user1 in result
    assert user2 in result