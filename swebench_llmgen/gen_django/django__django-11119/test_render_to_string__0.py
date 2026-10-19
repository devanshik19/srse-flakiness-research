import pytest
from django.template import Template, Engine
from django.template.context import Context
from django.contrib.auth.models import User


@pytest.fixture
def engine():
    return Engine(dirs=[], app_dirs=False, context_processors=[], debug=False, loaders=[], 
                  string_if_invalid='', file_charset='utf-8', libraries={}, builtins=[], autoescape=False)


@pytest.mark.parametrize("template_name, context, expected", [
    ("<h1>Hello {{ name }}</h1>", {'name': 'World'}, "<h1>Hello World</h1>"),
    (["<h1>Hello {{ name }}</h1>", "<h1>Fallback</h1>"], {'name': 'Django'}, "<h1>Hello Django</h1>"),
    (["non_existent_template.html"], None, None),  # To check template not found scenario
])
def test_render_to_string(engine, template_name, context, expected, monkeypatch):
    if expected is None:
        monkeypatch.setattr(engine, 'get_template', lambda name: Template("Template not found"))
    
    # Handle both template cases
    if isinstance(template_name, (list, tuple)):
        monkeypatch.setattr(engine, 'select_template', lambda names: Template(names[0]))
    else:
        monkeypatch.setattr(engine, 'get_template', lambda name: Template(template_name))

    if context is not None and not isinstance(context, Context):
        context = Context(context)

    result = engine.render_to_string(template_name, context)

    if expected is not None:
        assert result == expected
    else:
        assert "Template not found" in result  # Ensure we handle missing templates