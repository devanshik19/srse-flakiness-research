import pytest
from django.utils.functional import Promise
from django.contrib.auth.models import User
import enum

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

class UserChoices(enum.Enum, metaclass=ChoicesMeta):
    ADMIN = (1, "Admin")
    MODERATOR = (2, "Moderator")
    USER = (3, "User")
    UNKNOWN = (4,)

def test_choices_meta_new():
    # Test that the labels are created correctly
    assert UserChoices.ADMIN.label == "Admin"
    assert UserChoices.MODERATOR.label == "Moderator"
    assert UserChoices.USER.label == "User"
    assert UserChoices.UNKNOWN.label == "Unknown"

    # Test value to label map
    assert UserChoices._value2label_map_[1] == "Admin"
    assert UserChoices._value2label_map_[2] == "Moderator"
    assert UserChoices._value2label_map_[3] == "User"
    assert UserChoices._value2label_map_[4] == "Unknown"

    # Test for a label property
    admin_choice = UserChoices.ADMIN
    assert admin_choice.label == "Admin"
    
    # Test for str and Promise types
    promise = Promise('Active')
    ActiveChoices = enum.Enum('ActiveChoices', {
        'ACTIVE': (1, promise),
        'INACTIVE': (2, "Inactive")
    }, type=ChoicesMeta)
    assert ActiveChoices.ACTIVE.label == "Active"
    assert ActiveChoices.INACTIVE.label == "Inactive"