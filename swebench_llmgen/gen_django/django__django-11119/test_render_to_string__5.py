import pytest
from django.template import Engine
from django.template import Context
from django.contrib.auth.models import User
from django.template.exceptions import TemplateDoesNotExist

@pytest.fixture
def engine():
    return Engine(dirs=['./templates'], app_dirs=True, context_processors=[], debug=True, loaders=[], 
                  string_if_invalid='', file_charset='utf-8', libraries={}, builtins=[], autoescape=True)

def test_render_to_string_single_template(engine):
    # Create a simple template and save it
    with open('./templates/test_template.html', 'w') as f:
        f.write('Hello {{ user.username }}!')

    user = User.objects.create_user(username='testuser')
    context = {'user': user}

    result = engine.render_to_string('test_template.html', context)
    assert result == 'Hello testuser!'

def test_render_to_string_template_from_list(engine):
    # Create the same template and save it
    with open('./templates/test_template.html', 'w') as f:
        f.write('Hello {{ user.username }}!')

    user = User.objects.create_user(username='testuser')
    context = {'user': user}

    result = engine.render_to_string(['test_template.html'], context)
    assert result == 'Hello testuser!'

def test_render_to_string_context_as_context_instance(engine):
    # Create a simple template and save it
    with open('./templates/test_template.html', 'w') as f:
        f.write('Hello {{ user.username }}!')
    
    user = User.objects.create_user(username='testuser')
    context_instance = Context({'user': user})

    result = engine.render_to_string('test_template.html', context_instance)
    assert result == 'Hello testuser!'

def test_render_to_string_template_not_exist(engine):
    with pytest.raises(TemplateDoesNotExist):
        engine.render_to_string('non_existent_template.html', {})

def test_render_to_string_empty_context(engine):
    # Create a simple template and save it
    with open('./templates/test_template.html', 'w') as f:
        f.write('Hello World!')

    result = engine.render_to_string('test_template.html', None)
    assert result == 'Hello World!'