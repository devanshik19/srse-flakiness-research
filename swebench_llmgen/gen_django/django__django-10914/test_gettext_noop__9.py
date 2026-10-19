import pytest

from django.conf.global_settings import gettext_noop

def test_gettext_noop():
    input_str = "Hello, World!"
    output_str = gettext_noop(input_str)
    assert output_str == input_str

    empty_str = ""
    output_empty = gettext_noop(empty_str)
    assert output_empty == empty_str

    special_char_str = "¡Hola! ¿Cómo estás?"
    output_special = gettext_noop(special_char_str)
    assert output_special == special_char_str