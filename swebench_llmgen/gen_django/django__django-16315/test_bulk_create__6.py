import pytest
from django.contrib.auth.models import User
from django.db import transaction

@pytest.mark.parametrize("objs, batch_size, ignore_conflicts, update_conflicts, update_fields, unique_fields, expected_count", [
    ([], None, False, False, None, None, 0),  # Test empty list
    ([User(username='user1')], None, False, False, None, None, 1),  # Test single object
    ([User(username='user2'), User(username='user3')], None, False, False, None, None, 2),  # Test multiple objects
    ([User(username='user4'), User(username='user4')], None, True, False, None, None, 1),  # Test ignore_conflicts
])
def test_bulk_create(objs, batch_size, ignore_conflicts, update_conflicts, update_fields, unique_fields, expected_count):
    queryset = User.objects
    created_objs = queryset.bulk_create(objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts,
                                         update_conflicts=update_conflicts, update_fields=update_fields,
                                         unique_fields=unique_fields)
    
    # Verify the count of created objects
    assert queryset.count() == expected_count
    
    # Verify that created objects have the correct state
    for obj in created_objs:
        assert obj.pk is not None  # Ensure primary key is set for created users
        assert obj.username in ['user1', 'user2', 'user3', 'user4']
        
    if update_conflicts:
        # Test update conflicts
   
        conflicted_user = User(username='user4')
        queryset.bulk_create([conflicted_user], ignore_conflicts=ignore_conflicts, update_conflicts=update_conflicts)
        assert queryset.count() == expected_count  # Count should not change