import pytest
from django.template import Engine
from django.template import Context
from django.contrib.auth.models import User
from django.template import Template

@pytest.fixture
def engine():
    return Engine(dirs=[], app_dirs=False, context_processors=[], debug=False, 
                  loaders=[], string_if_invalid='', file_charset=None, 
                  libraries=[], builtins=[], autoescape=False)

@pytest.fixture
def simple_template():
    return Template("Hello, {{ user.username }}!")

def test_render_to_string_with_single_template(engine, simple_template):
    context = {'user': User(username='testuser')}
    output = engine.render_to_string(simple_template.name, context)
    assert output == "Hello, testuser!"

def test_render_to_string_with_context_instance(engine, simple_template):
    user_context = Context({'user': User(username='testuser')})
    output = engine.render_to_string(simple_template.name, user_context)
    assert output == "Hello, testuser!"

def test_render_to_string_with_template_list(engine, simple_template):
    # First we need to register the template with a mock loader (simplified for testing)
    engine.get_template = lambda name: simple_template
    context = {'user': User(username='testuser')}
    output = engine.render_to_string([simple_template.name], context)
    assert output == "Hello, testuser!"