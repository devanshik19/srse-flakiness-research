import pytest
from django.template.engine import Engine
from django.template import Context
from django.contrib.auth.models import User
from django.template import Template

@pytest.fixture
def engine():
    return Engine(dirs=[], app_dirs=False, context_processors=[], debug=False, loaders=[],
                  string_if_invalid='', file_charset=None, libraries=None, builtins=None, autoescape=True)

@pytest.fixture
def simple_template():
    return Template('Hello, {{ user.username }}!')

def test_render_to_string_with_single_template(engine, simple_template):
    template_name = simple_template.name if hasattr(simple_template, 'name') else 'simple_template'
    context = {'user': User(username='testuser')}
    
    # Simulate adding the template to the engine 
    engine.get_template = lambda name: simple_template
    rendered = engine.render_to_string(template_name, context)
    
    assert rendered == 'Hello, testuser!'

def test_render_to_string_with_template_list(engine, simple_template):
    template_name_list = [simple_template.name if hasattr(simple_template, 'name') else 'simple_template']
    context = {'user': User(username='testuser')}
    
    # Simulate adding the template to the engine 
    engine.select_template = lambda name_list: simple_template
    rendered = engine.render_to_string(template_name_list, context)
    
    assert rendered == 'Hello, testuser!'

def test_render_to_string_with_context_instance(engine, simple_template):
    template_name = simple_template.name if hasattr(simple_template, 'name') else 'simple_template'
    user = User(username='testuser')
    context = Context({'user': user})
    
    # Simulate adding the template to the engine 
    engine.get_template = lambda name: simple_template
    rendered = engine.render_to_string(template_name, context)
    
    assert rendered == 'Hello, testuser!'