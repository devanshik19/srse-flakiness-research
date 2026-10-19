import pytest
from django.template import Engine
from django.template import Context
from django.contrib.auth.models import User
from django.template.backends.django import DjangoTemplates

@pytest.fixture
def template_engine():
    return Engine(dirs=['/templates'], app_dirs=False, context_processors=[], debug=False,
                  loaders=[])

@pytest.fixture
def mock_template(template_engine):
    template_code = "Hello, {{ user.username }}!"
    template_name = 'greeting.html'
    engine = DjangoTemplates(engine=template_engine)
    engine.engine.template_source_loaders = []
    engine.engine.get_template(template_name).render = lambda context: template_code.format(**context)
    return template_name

@pytest.mark.parametrize("template_name, context, expected_output", [
    ('greeting.html', {'user': User(username='testuser')}, "Hello, testuser!"),
    (['greeting.html'], {'user': User(username='testuser')}, "Hello, testuser!"),
    ('greeting.html', Context({'user': User(username='testuser')}), "Hello, testuser!"),
])
def test_render_to_string(template_engine, mock_template, template_name, context, expected_output):
    output = template_engine.render_to_string(template_name, context)
    assert output == expected_output

def test_render_to_string_with_list(template_engine, mock_template):
    output = template_engine.render_to_string(['greeting.html'], {'user': User(username='testuser')})
    assert output == "Hello, testuser!"
    
def test_render_to_string_with_invalid_template(template_engine):
    with pytest.raises(TemplateDoesNotExist):
        template_engine.render_to_string('non_existent_template.html', {})