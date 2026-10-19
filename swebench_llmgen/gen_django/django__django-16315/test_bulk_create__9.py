import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

@pytest.mark.parametrize("objs, batch_size, ignore_conflicts, update_conflicts, expected_count", [
    ([User(username='user1'), User(username='user2')], None, False, False, 2),
    ([User(username='user1'), User(username='user1')], None, True, False, 1),  # Conflict case with ignore
    ([User(username='user1'), User(username='user2')], 1, False, False, 2),
    ([User(username='user1'), User(username='user2'), User(username='user1')], None, False, True, 2),  # Update case
])
def test_bulk_create(objs, batch_size, ignore_conflicts, update_conflicts, expected_count):
    queryset = User.objects
    original_count = queryset.count()
    
    # Prepare objects if updating
    if update_conflicts:
        for obj in objs:
            obj.pk = User.objects.filter(username=obj.username).first().id if User.objects.filter(username=obj.username).exists() else None

    result = queryset.bulk_create(objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts, update_conflicts=update_conflicts)
    
    assert len(result) == expected_count
    assert queryset.count() == original_count + expected_count

def test_bulk_create_invalid_batch_size():
    queryset = User.objects
    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        queryset.bulk_create([User(username='user1')], batch_size=0)
        
def test_bulk_create_multi_table_inheritance():
    class UserProfile(User):
        class Meta:
            proxy = True

    queryset = UserProfile.objects
    with pytest.raises(ValueError, match="Can't bulk create a multi-table inherited model"):
        queryset.bulk_create([UserProfile(username='user1')])