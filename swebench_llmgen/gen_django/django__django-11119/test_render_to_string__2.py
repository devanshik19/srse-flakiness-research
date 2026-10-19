import pytest
from django.contrib.auth.models import User
from django.template import Engine, Context, Template
from django.template.exceptions import TemplateDoesNotExist

@pytest.fixture
def engine():
    return Engine(dirs=['/path/to/templates'])

@pytest.fixture
def sample_template(engine):
    template_content = "Hello, {{ username }}!"
    template = Template(template_content)
    engine.get_template = lambda name: template
    return template

def test_render_to_string_with_single_template(engine, sample_template):
    context = {'username': 'Alice'}
    result = engine.render_to_string('sample_template.html', context)
    assert result == "Hello, Alice!"

def test_render_to_string_with_context_instance(engine, sample_template):
    context = Context({'username': 'Bob'})
    result = engine.render_to_string('sample_template.html', context)
    assert result == "Hello, Bob!"

def test_render_to_string_with_template_list(engine, sample_template):
    context = {'username': 'Charlie'}
    result = engine.render_to_string(['sample_template.html'], context)
    assert result == "Hello, Charlie!"

def test_render_to_string_template_does_not_exist(engine):
    with pytest.raises(TemplateDoesNotExist):
        engine.render_to_string('non_existent_template.html')

def test_render_to_string_with_no_context(engine, sample_template):
    result = engine.render_to_string('sample_template.html')
    assert result == "Hello, !"