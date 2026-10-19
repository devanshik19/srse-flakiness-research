import pytest
from django.core.management import CommandError
from django.core.management.commands.makemigrations import Command

def test_add_arguments():
    command = Command()
    parser = command.create_parser('test', 'makemigrations')

    # Check for default arguments
    default_args = [
        'app_label',
        '--dry-run',
        '--merge',
        '--empty',
        '--noinput',
        '-n',
        '--no-header',
        '--check',
        '--scriptable',
        '--update',
    ]
    
    for arg in default_args:
        assert arg in parser._actions[0].option_strings or arg in parser._actions[1].option_strings

    # Check if positional arguments are correctly added
    assert parser.usage.startswith('usage: test makemigrations [options] app_label')
    
    # Check specific arguments help descriptions
    help_texts = {
        "app_label": "Specify the app label(s) to create migrations for.",
        "--dry-run": "Just show what migrations would be made; don't actually write them.",
        "--merge": "Enable fixing of migration conflicts.",
        "--empty": "Create an empty migration.",
        "--noinput": "Tells Django to NOT prompt the user for input of any kind.",
        "-n": "Use this name for migration file(s).",
        "--no-header": "Do not add header comments to new migration file(s).",
        "--check": "Exit with a non-zero status if model changes are missing migrations.",
        "--scriptable": "Divert log output and input prompts to stderr, writing only paths of generated migration files to stdout.",
        "--update": "Merge model changes into the latest migration and optimize the resulting operations.",
    }

    for arg, description in help_texts.items():
        action = next((a for a in parser._actions if arg in a.option_strings), None)
        assert action is not None
        assert action.help == description