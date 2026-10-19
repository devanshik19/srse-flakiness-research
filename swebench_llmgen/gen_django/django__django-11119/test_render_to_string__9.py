import pytest
from django.template import Engine, Context
from django.contrib.auth.models import User
from django.template import TemplateDoesNotExist

@pytest.fixture
def engine():
    return Engine(dirs=['.'], app_dirs=True, context_processors=[], debug=True, loaders=[], string_if_invalid='', file_charset='', libraries=[], builtins=[], autoescape=False)

def test_render_to_string_single_template(engine):
    template_code = "Hello, {{ user.username }}!"
    template = engine.from_string(template_code)
    template_name = "user_template"
    # We need to create a valid template association
    engine.get_template = lambda name: template if name == template_name else None

    user = User(username='testuser')
    context = {'user': user}
    result = engine.render_to_string(template_name, context)

    assert result == "Hello, testuser!"

def test_render_to_string_multiple_templates(engine):
    template_code1 = "Hi, {{ user.username }}!"
    template_code2 = "Welcome, {{ user.username }}!"
    
    template1 = engine.from_string(template_code1)
    template2 = engine.from_string(template_code2)
    template_names = ["user_template1", "user_template2"]
    
    # Mocking the method to return templates based on names
    engine.get_template = lambda name: template1 if name == template_names[0] else (template2 if name == template_names[1] else None)

    user = User(username='testuser')
    context = {'user': user}
    
    result1 = engine.render_to_string(template_names[0], context)
    result2 = engine.render_to_string(template_names[1], context)
    
    assert result1 == "Hi, testuser!"
    assert result2 == "Welcome, testuser!"

def test_render_to_string_with_context_instance(engine):
    template_code = "Hello, {{ user.username }}!"
    template = engine.from_string(template_code)
    engine.get_template = lambda name: template

    user = User(username='testuser')
    context = Context({'user': user})
    
    result = engine.render_to_string("user_template", context)

    assert result == "Hello, testuser!"

def test_render_to_string_template_does_not_exist(engine):
    with pytest.raises(TemplateDoesNotExist):
        engine.render_to_string("non_existent_template")