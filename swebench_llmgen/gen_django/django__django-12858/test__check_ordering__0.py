import pytest
from django.core import checks
from django.db import models
from django.contrib.auth.models import User


class TestModelOrderingChecks:

    @pytest.mark.parametrize("ordering,expected_error_count", [
        (None, 0),
        ([], 0),
        (['username'], 0),
        (['-username'], 0),
        (['username', '-email'], 0),
        (['username', 'nonexistent_field'], 1),  # invalid field
        ([{'field': 'username'}], 1),  # not a list/tuple
        (['username', '?'], 0),
        (['username', 'related_model__field'], 0),  # valid related field
        (['related_model__nonexistent_field'], 1)  # invalid related field
    ])
    def test_check_ordering(self, ordering, expected_error_count):
        class ModelWithOrdering(models.Model):
            username = models.CharField(max_length=30)
            email = models.EmailField()
            related_model = models.ForeignKey(User, on_delete=models.CASCADE)

            class Meta:
                ordering = ordering if ordering is not None else None

        errors = ModelWithOrdering._check_ordering()
        assert len(errors) == expected_error_count

        if expected_error_count > 0:
            for error in errors:
                assert isinstance(error, checks.Error)
                assert error.id == 'models.E015' or error.id == 'models.E014'