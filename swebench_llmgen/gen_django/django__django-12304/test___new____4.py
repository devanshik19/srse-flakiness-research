import pytest
import enum
from django.utils.functional import Promise
from django.contrib.auth.models import User

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

class TestChoicesMeta(enum.Enum, metaclass=ChoicesMeta):
    FIRST_OPTION = 1, 'First Option'
    SECOND_OPTION = 2, 'Second Option'
    DEFAULT_OPTION = 3

def test_choices_meta_new_method():
    assert TestChoicesMeta.FIRST_OPTION.label == 'First Option'
    assert TestChoicesMeta.SECOND_OPTION.label == 'Second Option'
    assert TestChoicesMeta.DEFAULT_OPTION.label == 'Default Option'

    assert 'FIRST_OPTION' in TestChoicesMeta
    assert 'SECOND_OPTION' in TestChoicesMeta
    assert 'DEFAULT_OPTION' in TestChoicesMeta

    assert TestChoicesMeta._value2label_map_[1] == 'First Option'
    assert TestChoicesMeta._value2label_map_[2] == 'Second Option'
    assert TestChoicesMeta._value2label_map_[3] == 'Default Option'

    with pytest.raises(KeyError):
        assert TestChoicesMeta._value2label_map_[4]  # Non-existing value