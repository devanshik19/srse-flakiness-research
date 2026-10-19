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

class UserStatus(enum.Enum, metaclass=ChoicesMeta):
    ACTIVE = 1, 'Active'
    INACTIVE = 2, 'Inactive'
    PENDING_APPROVAL = 3, Promise('Pending Approval')

def test_choices_meta_new():

    # Check that the labels are set correctly
    assert UserStatus.ACTIVE.label == 'Active'
    assert UserStatus.INACTIVE.label == 'Inactive'
    assert UserStatus.PENDING_APPROVAL.label == 'Pending Approval'

    # Verify the values correspond to the correct enum members
    assert UserStatus(1) == UserStatus.ACTIVE
    assert UserStatus(2) == UserStatus.INACTIVE
    assert UserStatus(3) == UserStatus.PENDING_APPROVAL

    # Check the _value2label_map_ for accurate associations
    assert UserStatus._value2label_map_ == {
        1: 'Active',
        2: 'Inactive',
        3: 'Pending Approval'
    }