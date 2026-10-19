import pytest
from django.utils.functional import Promise
from django.contrib.auth.models import User
import enum

# Mocking the ChoicesMeta class for testing purposes
class ChoicesMeta(enum.EnumMeta):
    def __new__(metacls, classname, bases, classdict):
        labels = []
        for key in classdict._member_names:
            value = classdict[key]
            if (
                isinstance(value, (list, tuple)) and
                len(value) > 1 and
                isinstance(value[-1], (Promise, str))
            ):
                *value, label = value
                value = tuple(value)
            else:
                label = key.replace('_', ' ').title()
            labels.append(label)
            dict.__setitem__(classdict, key, value)
        cls = super().__new__(metacls, classname, bases, classdict)
        cls._value2label_map_ = dict(zip(cls._value2member_map_, labels))
        cls.label = property(lambda self: cls._value2label_map_.get(self.value))
        return enum.unique(cls)

# Creating a test Enum subclass to utilize ChoicesMeta
class TestEnum(enum.Enum, metaclass=ChoicesMeta):
    FIRST_OPTION = 1, 'First Option'
    SECOND_OPTION = 2
    THIRD_OPTION = 3, 'Third Option'

def test_choices_meta_new():
    # Test that the ChoicesMeta class properly initializes member labels
    assert TestEnum.FIRST_OPTION == 1
    assert TestEnum.SECOND_OPTION == 2
    assert TestEnum.THIRD_OPTION == 3
    assert TestEnum.FIRST_OPTION.label == 'First Option'
    assert TestEnum.SECOND_OPTION.label == 'Second Option'
    assert TestEnum.THIRD_OPTION.label == 'Third Option'

    # Validate the internal map of values to labels
    assert TestEnum._value2label_map_ == {
        1: 'First Option',
        2: 'Second Option',
        3: 'Third Option'
    }

    # Check if the label property returns the correct values
    assert TestEnum.FIRST_OPTION.label == 'First Option'
    assert TestEnum.SECOND_OPTION.label == 'Second Option'
    assert TestEnum.THIRD_OPTION.label == 'Third Option'