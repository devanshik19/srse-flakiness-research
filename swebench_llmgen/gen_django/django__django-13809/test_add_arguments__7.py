import pytest
from argparse import ArgumentParser
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.mark.parametrize("argument, expected_dest", [
    ('addrport', None),  # addrport doesn't have a specified 'dest'
    ('--ipv6', 'use_ipv6'),
    ('--nothreading', 'use_threading'),
    ('--noreload', 'use_reloader'),
])
def test_add_arguments(argument, expected_dest):
    command = Command()
    parser = ArgumentParser()
    
    command.add_arguments(parser)
    args, unknown = parser.parse_known_args([argument])

    # Check if the expected argument is successfully added
    if expected_dest:
        assert getattr(args, expected_dest) is not None
    else:
        assert args.addrport is not None