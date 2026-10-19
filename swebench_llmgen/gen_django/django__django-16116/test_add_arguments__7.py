import argparse
import pytest
from django.core.management import CommandError
from django.core.management.commands.makemigrations import Command

@pytest.fixture
def command():
    return Command()

def test_add_arguments(command):
    parser = argparse.ArgumentParser()
    command.add_arguments(parser)
    
    # Test the presence of required arguments
    args = parser.parse_args(["app_label"])
    assert args.args == ["app_label"]
    
    # Test default values for optional arguments
    assert not args.dry_run
    assert not args.merge
    assert not args.empty
    assert args.interactive
    assert args.name is None
    assert args.include_header
    assert not args.check_changes
    assert not args.scriptable
    assert not args.update
    
    # Parse with some optional arguments
    args = parser.parse_args([
        "app_label", 
        "--dry-run", 
        "--merge", 
        "--empty", 
        "--noinput", 
        "--name", "my_migration", 
        "--no-header", 
        "--check", 
        "--scriptable", 
        "--update"
    ])
    
    # Test values when options are set
    assert args.dry_run
    assert args.merge
    assert args.empty
    assert not args.interactive
    assert args.name == "my_migration"
    assert not args.include_header
    assert args.check_changes
    assert args.scriptable
    assert args.update