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


class Choices(enum.Enum, metaclass=ChoicesMeta):
    OPTION_ONE = 1, 'Option One'
    OPTION_TWO = 2, 'Option Two'
    OPTION_THREE = 3  # should default label


def test_choices_meta_new_with_label():
    assert Choices.OPTION_ONE.label == 'Option One'
    assert Choices.OPTION_TWO.label == 'Option Two'


def test_choices_meta_new_without_label():
    assert Choices.OPTION_THREE.label == 'Option Three'


def test_choices_meta_new_with_no_values():
    class EmptyChoices(enum.Enum, metaclass=ChoicesMeta):
        pass

    assert not EmptyChoices._value2label_map_