import pytest
from django.core.management import CommandError
from django.core.management import BaseCommand, call_command
from argparse import ArgumentParser

@pytest.fixture
def command():
    return BaseCommand()

def test_add_arguments_address_and_port(command):
    parser = ArgumentParser()
    command.add_arguments(parser)
    args = parser.parse_args(['127.0.0.1:8000'])
    assert args.addrport == '127.0.0.1:8000'

def test_add_arguments_ipv6(command):
    parser = ArgumentParser()
    command.add_arguments(parser)
    args = parser.parse_args(['--ipv6'])
    assert args.use_ipv6 is True

def test_add_arguments_nothreading(command):
    parser = ArgumentParser()
    command.add_arguments(parser)
    args = parser.parse_args(['--nothreading'])
    assert args.use_threading is False

def test_add_arguments_noreload(command):
    parser = ArgumentParser()
    command.add_arguments(parser)
    args = parser.parse_args(['--noreload'])
    assert args.use_reloader is False

def test_add_arguments_no_args(command):
    parser = ArgumentParser()
    command.add_arguments(parser)
    args = parser.parse_args([])
    assert args.addrport is None
    assert args.use_ipv6 is False
    assert args.use_threading is True
    assert args.use_reloader is True