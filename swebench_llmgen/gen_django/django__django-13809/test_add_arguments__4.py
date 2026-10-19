import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

def test_add_arguments():
    # Create an instance of the Command class
    command = Command()
    
    # Create a parser object
    from argparse import ArgumentParser
    parser = ArgumentParser()
    
    # Call the add_arguments method
    command.add_arguments(parser)
    
    # Test that the correct arguments are added
    args = parser.parse_args(['addrport'])
    assert args.addrport == 'addrport'
    assert args.use_ipv6 is False
    assert args.use_threading is True
    assert args.use_reloader is True

    # Test parsing with additional arguments
    args = parser.parse_args(['addrport', '--ipv6', '--nothreading', '--noreload'])
    assert args.addrport == 'addrport'
    assert args.use_ipv6 is True
    assert args.use_threading is False
    assert args.use_reloader is False