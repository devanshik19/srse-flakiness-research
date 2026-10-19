import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Field

class TestField(Field):
    def to_python(self, value):
        if value in (None, ''):
            return None
        return super().to_python(value)

@pytest.mark.parametrize("input_value, expected_output", [
    (None, None),
    ('', None),
    ('valid_value', 'valid_value'),
    (123, 123),
    (3.14, 3.14),
    (datetime.datetime.now(), datetime.datetime.now().replace(microsecond=0)),
    (datetime.date.today(), datetime.date.today()),
    (uuid.uuid4(), uuid.uuid4()),
    (decimal.Decimal('3.14'), decimal.Decimal('3.14')),
])
def test_to_python(input_value, expected_output):
    field = TestField()
    if isinstance(input_value, datetime.datetime):
        result = field.to_python(input_value)
        assert result.replace(microsecond=0) == expected_output.replace(microsecond=0)
    elif isinstance(input_value, uuid.UUID):
        assert field.to_python(input_value) == expected_output
    else:
        assert field.to_python(input_value) == expected_output

def test_to_python_raises_validation_error():
    field = TestField()
    with pytest.raises(ValidationError):
        field.to_python(object())