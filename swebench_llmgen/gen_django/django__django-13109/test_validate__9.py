import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class ForeignKey(models.Field):
    def __init__(self, to, on_delete, related_name=None, **kwargs):
        self.remote_field = models.ManyToOneRel(
            model=to,
            field_name='id',
            related_name=related_name,
            on_delete=on_delete,
        )
        super().__init__(**kwargs)

    def validate(self, value, model_instance):
        if self.remote_field.parent_link:
            return
        super().validate(value, model_instance)
        if value is None:
            return

        using = router.db_for_read(self.remote_field.model, instance=model_instance)
        qs = self.remote_field.model._default_manager.using(using).filter(
            **{self.remote_field.field_name: value}
        )
        qs = qs.complex_filter(self.get_limit_choices_to())
        if not qs.exists():
            raise ValidationError(
                {'invalid': 'The related object does not exist.'},
                code='invalid',
                params={
                    'model': self.remote_field.model._meta.verbose_name,
                    'pk': value,
                    'field': self.remote_field.field_name,
                    'value': value,
                },
            )

# Test cases
def test_foreign_key_validation_existing_user():
    user = User.objects.create(username='testuser')
    fk_field = ForeignKey(User, on_delete=models.CASCADE)
    fk_field.validate(user.id, None)

def test_foreign_key_validation_nonexistent_user():
    fk_field = ForeignKey(User, on_delete=models.CASCADE)
    with pytest.raises(ValidationError) as excinfo:
        fk_field.validate(999, None)  # Assuming 999 is a non-existent ID
    assert excinfo.value.messages == [{'invalid': 'The related object does not exist.'}]