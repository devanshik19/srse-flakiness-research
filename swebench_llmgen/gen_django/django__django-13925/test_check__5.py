import pytest
from django.contrib.auth.models import User
from django.db import models

class TestModelCheck:

    def test_check_with_swappable(self):
        user = User.objects.create_user(username='testuser', password='password')
        errors = User.check()

        assert isinstance(errors, list)
        assert len(errors) == 0  # No errors expected for a valid model

    def test_check_with_swapped(self):
        class SwappedUser(User):
            class Meta:
                swappable = True
        errors = SwappedUser.check()

        assert isinstance(errors, list)
        assert len(errors) > 0  # Expected to have errors since it considers swappable

    def test_check_id_field(self):
        user = User.objects.create_user(username='testuser', password='password')
        user._meta.pk = None  # Simulate no primary key
        errors = User.check()

        assert isinstance(errors, list)
        assert any("id" in str(error) for error in errors)

    def test_check_field_name_clashes(self):
        # Assuming User has a field 'username', we simulate a clash
        User._meta.get_field('username').name = 'id'  # Simulate clash
        errors = User.check()

        assert isinstance(errors, list)
        assert any("field name clashes" in str(error) for error in errors)

    def test_check_constraints(self):
        # Simulating a check in constraints
        User._meta.constraints.append(
            models.UniqueConstraint(fields=['username'], name='unique_username')
        )
        errors = User.check()

        assert isinstance(errors, list)
        assert len(errors) == 0  # No errors expected after adding valid constraints