import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

@pytest.mark.parametrize("args, expected", [
    (["addrport"], True),
    (["addrport", "--ipv6"], True),
    (["addrport", "--nothreading"], True),
    (["addrport", "--noreload"], True),
    ([], False),
])
def test_add_arguments(args, expected):
    command = Command()
    parser = command.create_parser('manage.py', 'runserver')
    
    # Add arguments using the method to be tested
    command.add_arguments(parser)
    
    # Check if the expected arguments are added to the parser
    if expected:
        for arg in args:
            assert any(arg in action.dest for action in parser._actions)
    else:
        assert len(parser._actions) == 0