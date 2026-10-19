import pytest
from django.contrib.auth.models import User
from django.contrib.admin import ModelAdmin
from django.db import models
from django.core.exceptions import FieldDoesNotExist

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class TestModelAdmin(ModelAdmin):
    model = TestModel
    list_filter = ['user']
    date_hierarchy = 'id'

    def lookup_allowed(self, lookup, value):
        # Implementation of lookup_allowed (copied from provided source)
        from django.contrib.admin.filters import SimpleListFilter
        model = self.model
        for fk_lookup in model._meta.related_fkey_lookups:
            if callable(fk_lookup):
                fk_lookup = fk_lookup()
            if (lookup, value) in widgets.url_params_from_lookup_dict(fk_lookup).items():
                return True

        relation_parts = []
        prev_field = None
        for part in lookup.split(LOOKUP_SEP):
            try:
                field = model._meta.get_field(part)
            except FieldDoesNotExist:
                break
            if not prev_field or (prev_field.is_relation and field not in prev_field.path_infos[-1].target_fields):
                relation_parts.append(part)
            if not getattr(field, "path_infos", None):
                break
            prev_field = field
            model = field.path_infos[-1].to_opts.model

        if len(relation_parts) <= 1:
            return True
        valid_lookups = {self.date_hierarchy}
        for filter_item in self.list_filter:
            if isinstance(filter_item, type) and issubclass(filter_item, SimpleListFilter):
                valid_lookups.add(filter_item.parameter_name)
            elif isinstance(filter_item, (list, tuple)):
                valid_lookups.add(filter_item[0])
            else:
                valid_lookups.add(filter_item)

        return not {LOOKUP_SEP.join(relation_parts), LOOKUP_SEP.join(relation_parts + [part])}.isdisjoint(valid_lookups)


@pytest.mark.parametrize(
    'lookup, value, expected',
    [
        ('user', 1, True),                       # Valid local field
        ('user__id', 1, True),                   # Valid FK field lookup
        ('name', 'Test', True),                  # Valid local field
        ('wrong_field', 'value', True),          # Non-existent field
        ('user__profile', 'value', False),       # Non-existent relation
        ('user__environment', 'value', False),   # Non-existent field with relation
    ]
)
def test_lookup_allowed(lookup, value, expected):
    admin = TestModelAdmin(TestModel, None)
    assert admin.lookup_allowed(lookup, value) == expected